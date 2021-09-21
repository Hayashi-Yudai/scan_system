import datetime
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import numpy as np
import os

from core.utils.waveform import WaveForm
from core.utils import api_ops
from core.models import TDSData, TemporalData

# global variable
scan_running = False
tds_running = False


class RapidScan(View):
    def __init__(self):
        super(RapidScan, self).__init__()
        TemporalData.objects.filter(data_type="RAPID").delete()
        TemporalData.objects.create(data_type="RAPID")

    def get(self, request):
        return render(request, "core/index_rapid.html")


class StepScan(View):
    def __init__(self):
        super(StepScan, self).__init__()
        TemporalData.objects.filter(data_type="TDS").delete()
        TemporalData.objects.create(data_type="TDS")

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

    data_type = request.POST.get("type")
    present_data = (
        TemporalData.objects.filter(data_type=data_type).order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)
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
    present_data = (
        TemporalData.objects.filter(data_type="RAPID").order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)

    x = np.linspace(0, 8 * np.pi, 200)
    y = 1e-6 * np.sin(x)
    wave.x = x.tolist()
    wave.y = y.tolist()
    present_data.position_data = ",".join(list(map(str, wave.x)))
    present_data.intensity_data = ",".join(list(map(str, wave.y)))
    present_data.save()
    return JsonResponse(
        {"x": np.round(x, 2).tolist(), "y": y.tolist(), "running": False}
    )


def gpib(request) -> JsonResponse:
    intensity, connection = api_ops.get_lockin_intensity()
    return JsonResponse({"intensity": intensity, "connection": connection})


def calc_fft(request) -> JsonResponse:
    data_type = request.POST.get("type")
    present_data = (
        TemporalData.objects.filter(data_type=data_type).order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)

    if request.POST.get("fft") == "true":
        if len(wave.x) == 0:
            return JsonResponse({"x": [], "y": []})
        freq, fft = api_ops.calc_fft([wave.x, wave.y])  # (list, list)

        return JsonResponse({"x": freq, "y": fft})
    else:
        return JsonResponse({"x": wave.x, "y": wave.y})


def tds_boot(request) -> JsonResponse:
    global tds_running

    present_data = (
        TemporalData.objects.filter(data_type="TDS").order_by("-created_at").first()
    )
    present_data.position_data = ""
    present_data.intensity_data = ""

    tds_running = True
    start = int(request.POST.get("start"))
    end = int(request.POST.get("end"))
    step = int(request.POST.get("step"))
    lockin = float(request.POST.get("lockin"))

    success = api_ops.tds_scan(start, end, step, lockin, present_data)

    tds_running = False

    if success:
        data = TDSData(
            measured_date=datetime.datetime.now(),
            start_position=start,
            end_position=end,
            step=step,
            lockin_time=lockin,
            position_data=present_data.position_data,
            intensity_data=present_data.intensity_data,
            file_name="",
        )
        data.save()

    return JsonResponse({})


def tds_data(request) -> JsonResponse:
    present_data = (
        TemporalData.objects.filter(data_type="TDS").order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)
    status = "running" if tds_running else "finished"

    return JsonResponse({"x": wave.x, "y": wave.y, "status": status})


def change_sensitivity(request) -> JsonResponse:
    value = int(request.POST.get("value"))
    unit = request.POST.get("unit")
    api_ops.set_lockin_sensitivity(value, unit)

    return JsonResponse({"status": "ok"})


def change_time_const(request) -> JsonResponse:
    value = int(request.POST.get("value"))
    unit = request.POST.get("unit")
    api_ops.set_lockin_time_const(value, unit)

    return JsonResponse({"status": "ok"})


def auto_phase(request) -> JsonResponse:
    status = api_ops.auto_phase_lockin()
    print(status)

    return JsonResponse({"status": "ok"})
