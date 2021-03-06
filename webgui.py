import os
from datetime import datetime
import logging
import tempfile
import subprocess as sps
from threading import Lock, Thread

from scan_system.wsgi import application


logging.basicConfig(
    level=logging.INFO, format="flaskwebgui - [%(levelname)s] - %(message)s"
)


def find_chrome_win():
    # using edge by default since it's build on chromium
    edge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        return edge_path

    import winreg as reg

    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"

    chrome_path = None
    last_exception = None

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
        except WindowsError as e:
            last_exception = e
        else:
            if chrome_path and len(chrome_path) > 0:
                break

    # Only log some debug info if we failed completely to find chrome
    if not chrome_path:
        logging.exception(last_exception)
        logging.error("Failed to detect chrome location from registry")
    else:
        logging.info(f"Chrome path detected as: {chrome_path}")

    return chrome_path


def get_default_chrome_path():
    """
    Credits for get_instance_path, find_chrome_mac, find_chrome_linux, find_chrome_win funcs
    got from: https://github.com/ChrisKnott/Eel/blob/master/eel/chrome.py
    """
    return find_chrome_win()


current_timestamp = None


class FlaskUI:
    def __init__(
        self,
        app,
        width=800,
        height=600,
        maximized=False,
        fullscreen=False,
        browser_path=None,
        socketio=None,
        on_exit=None,
        idle_interval=5,
        close_server_on_exit=True,
    ) -> None:

        self.app = app
        self.width = str(width)
        self.height = str(height)
        self.fullscreen = fullscreen
        self.maximized = maximized
        self.browser_path = browser_path if browser_path else get_default_chrome_path()
        self.socketio = socketio
        self.on_exit = on_exit
        self.idle_interval = idle_interval
        self.close_server_on_exit = close_server_on_exit

        self.host = "127.0.0.1"
        self.port = 8000
        self.localhost = f"http://{self.host}:{self.port}"

        if self.close_server_on_exit:
            self.lock = Lock()

    def update_timestamp(self):
        self.lock.acquire()
        global current_timestamp
        current_timestamp = datetime.now()
        self.lock.release()

    def run(self):
        """
        Starts 3 threads one for webframework server and one for browser gui
        """

        if self.close_server_on_exit:
            self.update_timestamp()

        t_start_webserver = Thread(target=self.start_django)
        t_open_chromium = Thread(target=self.open_chromium)
        t_stop_webserver = Thread(target=self.stop_webserver)

        threads = [t_start_webserver, t_open_chromium, t_stop_webserver]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def start_django(self):
        try:
            import waitress

            waitress.serve(self.app, host=self.host, port=self.port)
        except ImportError:
            os.system(f"python manage.py runserver {self.port}")

    def open_chromium(self):
        """
        Open the browser selected (by default it looks for chrome)
        # https://peter.sh/experiments/chromium-command-line-switches/
        """

        logging.info(f"Opening browser at {self.localhost}")

        temp_profile_dir = os.path.join(tempfile.gettempdir(), "flaskwebgui")

        if self.browser_path:
            launch_options = None
            if self.fullscreen:
                launch_options = ["--start-fullscreen"]
            elif self.maximized:
                launch_options = ["--start-maximized"]
            else:
                launch_options = [f"--window-size={self.width},{self.height}"]

            options = (
                [
                    self.browser_path,
                    f"--user-data-dir={temp_profile_dir}",
                    "--new-window",
                    "--no-first-run",
                    # "--window-position=0,0"
                ]
                + launch_options
                + [f"--app={self.localhost}"]
            )

            sps.Popen(options, stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)

        else:
            import webbrowser

            webbrowser.open_new(self.localhost)

    def stop_webserver(self):

        if self.close_server_on_exit is False:
            return

        # TODO add middleware for Django
        logging.info("Middleware not implemented (yet) for Django.")
        return

    def keep_server_running(self):
        self.update_timestamp()
        return "Ok"


if __name__ == "__main__":
    FlaskUI(application, maximized=True).run()
