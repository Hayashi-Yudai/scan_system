import datetime
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import numpy as np
import os

from core.utils.waveform import WaveForm
from core.utils import api_ops
from core.models import TDSData

# global variable
wave = WaveForm()
wave_tds = WaveForm()
scan_running = False
tds_running = False


class RapidScan(View):
    def __init__(self, *args, **kwargs):
        super(RapidScan, self).__init__(*args, **kwargs)

        # TODO: Remove
        self.x = wave.x
        self.y = wave.y

    def get(self, request):
        # TODO: Remove
        wave.set([1, 2, 3, 4, 5, 6, 7], [1, 4, 9, 16, 25, 36, 49])
        self.x = wave.x
        self.y = wave.y

        # TODO: context is not necessary
        context = {"position": self.x, "intensity": self.y}

        return render(request, "core/index_rapid.html", context)

    # TODO: remove
    def post(self, request):
        context = {"position": self.x, "intensity": self.y}

        # TODO: context is not necessary
        return render(request, "core/index_rapid.html", context)


class StepScan(View):
    def get(self, request):
        return render(request, "core/index_step.html")


#####################################
# JSON APIs
#####################################


def move(request):
    position: int = int(request.POST.get("position"))
    succeed: bool = api_ops.move_stage(position)

    return JsonResponse({"success": succeed})


def save(request):
    save_path = request.POST.get("path")
    directory = save_path.rsplit("/", 1)[0]
    if not os.path.exists(directory):
        return JsonResponse({"success": False})

    if request.POST.get("type") == "TDS":
        api_ops.save_data_as_csv(save_path, [wave_tds.x, wave_tds.y])
    else:
        api_ops.save_data_as_csv(save_path, [wave.x, wave.y])

    data = TDSData.objects.order_by("-measured_date").first()
    data.file_name = save_path.rsplit("/", 1)[1]
    data.save()

    return JsonResponse({"success": True})


# TODO: A/Dコンバータでの処理と合わせる
def scan(request):
    duration = float(request.POST.get("duration"))
    sample_rate = float(request.POST.get("sampling_rate"))
    # if not scan_running
    #   output, scan_running = raster_scan(duration, sample_rate, scan_running)
    x = np.linspace(0, 8 * np.pi, 200)
    y = 1e-6 * np.sin(x)
    wave.x = x.tolist()
    wave.y = y.tolist()
    return JsonResponse(
        {"x": np.round(x, 2).tolist(), "y": y.tolist(), "running": False}
    )


def gpib(request):
    intensity, connection = api_ops.get_lockin_intensity()
    return JsonResponse({"intensity": intensity, "connection": connection})


def calc_fft(request):
    if request.POST.get("fft") == "true":
        if request.POST.get("type") == "RAPID":
            if len(wave.x) == 0:
                return JsonResponse({"x": [], "y": []})
            freq, fft = api_ops.calc_fft([wave.x, wave.y])  # (list, list)

            return JsonResponse({"x": freq, "y": fft})
        if request.POST.get("type") == "TDS":
            if len(wave_tds.x) == 0:
                return JsonResponse({"x": [], "y": []})
            freq, fft = api_ops.calc_fft([wave_tds.x, wave_tds.y])  # (list, list)

            return JsonResponse({"x": freq, "y": fft})
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

    success = api_ops.tds_scan(start, end, step, lockin, wave_tds)

    tds_running = False

    if success:
        data = TDSData(
            measured_date=datetime.datetime.now(),
            start_position=start,
            end_position=end,
            step=step,
            lockin_time=lockin,
            position_data=",".join(list(map(str, wave_tds.x))),
            intensity_data=",".join(list(map(str, wave_tds.y))),
            file_name="",
        )
        data.save()

    return JsonResponse({})


def tds_data(request):
    x = wave_tds.x
    y = wave_tds.y

    status = "running" if tds_running else "finished"

    return JsonResponse({"x": x, "y": y, "status": status})


def change_sensitivity(request):
    value = int(request.POST.get("value"))
    unit = request.POST.get("unit")
    api_ops.set_lockin_sensitivity(value, unit)

    return JsonResponse({"status": "ok"})


def change_time_const(request):
    value = int(request.POST.get("value"))
    unit = request.POST.get("unit")
    api_ops.set_lockin_time_const(value, unit)

    return JsonResponse({"status": "ok"})


def auto_phase(request):
    status = api_ops.auto_phase_lockin()
    print(status)

    return JsonResponse({"status": "ok"})
