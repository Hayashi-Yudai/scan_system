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
scan_running = False


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

    df = pd.DataFrame({"x": wave.x, "y": wave.y})

    if save_path.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        df.to_csv(save_path + ".csv", index=False)

    return JsonResponse({"success": True})


# TODO: A/Dコンバータでの処理と合わせる
# TODO: A/Dコンバータのデータ取り込み開始は一回だけ実行される必要がある
def scan(request):
    duration = request.POST.get("duration")
    sample_rate = request.POST.get("sampling_rate")
    # output = raster_scan(duration, sample_rate);
    x = [i for i in range(10)]
    y = [i ** 3 for i in range(10)]
    return JsonResponse({"x": x, "y": y, "running": False})


def gpib(request):
    try:
        with SR830(11) as sr830:
            intensity = float(sr830.get_intensity())
        connection = True
    except:
        intensity = 0
        connection = False
    return JsonResponse({"intensity": intensity, "connection": connection})
