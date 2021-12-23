from flaskwebgui import FlaskUI
from scan_system.wsgi import application

if __name__ == "__main__":
    FlaskUI(application, start_server="django", maximized=True).run()
