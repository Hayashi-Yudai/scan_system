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
        self.x = wave.x
        self.y = wave.y

    def get(self, request):
        wave.set(
            [1, 2, 3, 4, 5, 6, 7],
            [1, 4, 9, 16, 25, 36, 49]
        )
        self.x = wave.x
        self.y = wave.y

        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/raster.html', context)

    def post(self, request):
        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/raster.html', context)


class TDS(View):
    def get(self, request):
        return render(request, 'core/tds.html')

# JSON APIs


def move(request):
    position = int(request.POST.get("position"))
    succeed = False
    try:
        with Mark202() as stage:
            stage.move(position)

        succeed = True
    except Exception as e:
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
    duration = request.POST.get("duration")
    sample_rate = request.POST.get("sampling_rate")
    # if not scan_running
    #   output, scan_running = raster_scan(duration, sample_rate, scan_running)
    x = np.linspace(0, 8 * np.pi, 2500)
    y = np.sin(x)
    return JsonResponse({"x": np.round(x, 2).tolist(), "y": y.tolist(), "running": False})


def gpib(request):
    try:
        with SR830() as sr830:
            intensity = float(sr830.get_intensity())
        connection = True
    except:
        intensity = 0
        connection = False
    return JsonResponse({"intensity": intensity, "connection": connection})


def tds_validate(request):
    start = request.POST.get("start")
    end = request.POST.get("end")
    step = request.POST.get("step")
    lockin = request.POST.get("lockin")

    status = "ok"
    try:
        start = int(start)
        end = int(end)
        step = int(step)
        lockin = float(lockin)
        if start > end or start < 0 or end < 0 or step < 0 or lockin < 0:
            status = "NG"
    except Exception as e:
        status = "NG"

    return JsonResponse({"status": status})


def tds_boot(request):
    global tds_running

    tds_running = True
    wave_tds.clear()
    start = int(request.POST.get("start"))
    end = int(request.POST.get("end"))
    step = int(request.POST.get("step"))
    lockin = float(request.POST.get("lockin"))
    try:
        with SR830() as amp, Mark202() as stage:
            stage.move(start)
            stage.wait_while_busy()

            position_now = start
            while position_now <= end:
                time.sleep(lockin / 1000)
                intensity = amp.get_intensity()

                wave_tds.push([position_now], [intensity])
                stage.move(position_now + step)
                position_now += step
                stage.wait_while_busy()
    except Exception as e:
        print(e)

    tds_running = False

    return JsonResponse({})


def tds_data(request):
    x = wave_tds.x
    y = wave_tds.y

    status = "running" if tds_running else "finished"

    return JsonResponse({"x": x, "y": y, "status": status})
