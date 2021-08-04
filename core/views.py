import time
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import numpy as np
import os
import pandas as pd

from core.utils.waveform import WaveForm
from core.utils.SR830 import SR830
from core.utils.Mark202 import Mark202

# global variable
wave = WaveForm()
wave_tds = WaveForm()
scan_running = False
tds_running = False


class Index(View):
    def __init__(self, *args, **kwargs):
        super(Index, self).__init__(*args, **kwargs)

        # TODO: Remove
        self.x = wave.x
        self.y = wave.y

    def get(self, request):
        # TODO: Remove
        wave.set(
            [1, 2, 3, 4, 5, 6, 7],
            [1, 4, 9, 16, 25, 36, 49]
        )
        self.x = wave.x
        self.y = wave.y

        # TODO: context is not necessary
        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/raster.html', context)

    # TODO: remove
    def post(self, request):
        context = {"position": self.x, "intensity": self.y}

        # TODO: context is not necessary
        return render(request, 'core/raster.html', context)


class TDS(View):
    def get(self, request):
        return render(request, 'core/tds.html')


#####################################
# JSON APIs
#####################################


def move(request):
    position = int(request.POST.get("position"))
    succeed = False
    try:
        with Mark202(int(os.environ["MARK202_GPIB_ADDRESS"])) as stage:
            stage.move(position)

        succeed = True
    except Exception as e:
        print("Error occurred in move()")
        print(e)

    return JsonResponse({"success": succeed})


def save(request):
    save_path = request.POST.get("path")
    directory = save_path.rsplit("/", 1)[0]
    if not os.path.exists(directory):
        return JsonResponse({"success": False})

    if request.POST.get("type") == "TDS":
        df = pd.DataFrame({"x": wave_tds.x, "y": wave_tds.y})
    else:
        df = pd.DataFrame({"x": wave.x, "y": wave.y})

    if save_path.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        df.to_csv(save_path + ".csv", index=False)

    return JsonResponse({"success": True})


# TODO: A/Dコンバータでの処理と合わせる
def scan(request):
    duration = float(request.POST.get("duration"))
    sample_rate = float(request.POST.get("sampling_rate"))
    # if not scan_running
    #   output, scan_running = raster_scan(duration, sample_rate, scan_running)
    x = np.linspace(0, 8 * np.pi, 200)
    y = 1e-6*np.sin(x)
    wave.x = x
    wave.y = y
    return JsonResponse({"x": np.round(x, 2).tolist(), "y": y.tolist(), "running": False})


def gpib(request):
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as sr830:
            intensity = float(sr830.get_intensity())
        connection = True
    except:
        intensity = 0
        connection = False
    return JsonResponse({"intensity": intensity, "connection": connection})


def calc_fft(request):
    if request.POST.get('fft') == "true":
        if request.POST.get("type") == "RAPID":
            if len(wave.x) == 0:
                return JsonResponse({"x": [], "y": []})
            delta_time = (wave.x[1] - wave.x[0]) * 1e-6 * 2 / 2.9979e8
            print("wave.x = ", wave.x)
            freq = [i / delta_time / 4096 for i in range(4096)]
            fft = np.fft.fft(wave.y, 4096)

            return JsonResponse({"x": freq, "y": abs(fft).tolist()})
        if request.POST.get("type") == "TDS":
            if len(wave_tds.x) == 0:
                return JsonResponse({"x": [], "y": []})
            delta_time = (wave_tds.x[1] - wave_tds.x[0]) * 1e-6 * 2 / 2.9979e8
            freq = [i / delta_time / 4096 for i in range(4096)]
            fft = np.fft.fft(wave_tds.y, 4096)

            return JsonResponse({"x": freq, "y": abs(fft).tolist()})
    else:
        if request.POST.get("type") == "RAPID":
            return JsonResponse({"x": wave.x, "y": wave.y})
        elif request.POST.get("type") == "TDS":
            return JsonResponse({"x": wave_tds.x, "y": wave_tds.y})


def tds_boot(request):
    global tds_running

    tds_running = True
    wave_tds.clear()
    start = int(request.POST.get("start"))
    end = int(request.POST.get("end"))
    step = int(request.POST.get("step"))
    lockin = float(request.POST.get("lockin"))
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as amp, Mark202() as stage:
            stage.move(start)
            stage.wait_while_busy()

            position_now = start
            while position_now <= end:
                time.sleep(lockin / 1000)
                intensity = amp.get_intensity()

                wave_tds.push([position_now], [float(intensity)])
                stage.move(position_now + step)
                position_now += step
                stage.wait_while_busy()
    except Exception as e:
        print("Error in tds_boot()")
        print(e)

    tds_running = False

    return JsonResponse({})


def tds_data(request):
    x = wave_tds.x
    y = wave_tds.y

    status = "running" if tds_running else "finished"

    return JsonResponse({"x": x, "y": y, "status": status})
