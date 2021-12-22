import datetime
import os
from ctypes import cdll
import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View
import json

from core.models import TDSData, TemporalData
from core.utils import api_ops
from core.utils.waveform import WaveForm

# global variable
scan_running = False
tds_running = False

logger = logging.getLogger("root")


class RapidScan(View):
    """
    Get rapid scan page.
    """

    def __init__(self):
        super(RapidScan, self).__init__()
        TemporalData.objects.filter(data_type="RAPID").delete()
        TemporalData.objects.create(data_type="RAPID")

    def get(self, request):
        logger.debug("Core.RapidScan: GET")
        return render(request, "core/index_rapid.html")


class StepScan(View):
    """
    Get step scan page.
    """

    def __init__(self):
        super(StepScan, self).__init__()
        TemporalData.objects.filter(data_type="TDS").delete()
        TemporalData.objects.create(data_type="TDS")

    def get(self, request):
        logger.debug("Core.StepScan: GET")
        return render(request, "core/index_step.html")


#####################################
# JSON APIs
#####################################


def move(request) -> HttpResponse:
    """
    Move the step motor stage. The endpoint is `core/move/`.
    If the parameter is invalid, returns 404 Bad Request.

    :param django.http.HttpRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        - fields:
            - position: Target absolute position in micro-meter

    :returns:

        The result of the operation as JSON format.
        If succeeded, returns {"success": True}
        If bad request, returns 404 Bad Request
    """
    try:
        position = int(request.POST.get("position"))
        logging.debug(f"Core.move: position={position}")
    except (TypeError, ValueError) as e:
        logger.error(f"Core.move: raised TypeError or ValueError -> {e}")
        return HttpResponseBadRequest("Invalid parameter")

    if position < 0:
        logger.warning(f"Core.move: rejected position={position}")
        return HttpResponseBadRequest("'position' must be positive or zero")

    succeed: bool = api_ops.move_stage(position)
    logger.debug(f"Core.move: succeed={succeed}")

    return JsonResponse({"success": succeed})


def save(request) -> HttpResponse:
    """
    Save the measured data in CSV file. The endpoint is `core/save/`.
    If the parameter(s) is invalid, returns 404 Bad Request.

    :param django.http.HttpRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        - fields

            - path: The path to save data
            - type: The type of measurement. Choose "TDS" or "RAPID"

    :returns:

        The result of the operation as JSON format.
        If succeeded, returns {"success": True}
        If bad request, returns 404 Bad Request
    """
    if (save_path := request.POST.get("path")) is None:
        logger.debug("Core.save: path is None")
        return HttpResponseBadRequest("Invalid parameter")

    if save_path.count("/") < 1:
        logger.debug(f"Core.save: invalid path -> {save_path}")
        return HttpResponseBadRequest("Invalid path")

    directory = save_path.rsplit("/", 1)[0]
    if not os.path.exists(directory):
        logger.debug(f"Core.save: {directory} does not exist")
        return HttpResponseBadRequest("Invalid path")

    if (data_type := request.POST.get("type")) not in ["TDS", "RAPID"]:
        logger.debug(f"Core.save: Invalid type  {data_type}")
        return HttpResponseBadRequest("Invalid parameter")

    present_data = (
        TemporalData.objects.filter(data_type=data_type).order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)
    api_ops.save_data_as_csv(save_path, [wave.x, wave.y])

    data = TDSData.objects.order_by("-measured_date").first()
    data.file_name = save_path.rsplit("/", 1)[1]
    data.save()

    return JsonResponse({"success": True})


def gpib(request) -> JsonResponse:
    """
    Check the GPIB connection and returns Lockin amplifier's intensity.
    The endpoint is `core/gpib/`

    :param django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",

    :returns:
        The result of the operation as JSON format. JSON response contains,

        - intensity: The value of Lockin amplifier
        - connection: The existence of GPIB connection
    """
    intensity, connection = api_ops.get_lockin_intensity()  # float, bool
    logger.debug(f"Core.gpib: intensity = {intensity}")
    logger.debug(f"Core.gpib: connection = {connection}")
    return JsonResponse({"intensity": intensity, "connection": connection})


def calc_fft(request) -> JsonResponse:
    """
    Calculate the (inverse) Fourier transform with FFT algorithm.
    If choosing Fourier transform, the number of data points is expanded to be 4096.
    The endpoint is `core/fft-calc/`

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        - fields:

            - type (str): The type of data. Choose "TDS" or "RAPID".
            - fft: Whether calculating FFT or IFFT. Specify it with "true" or "false".

    :returns:
        The JSON data.

        - x: positional data or frequency.
        - y: intensity data.
    """
    if (data_type := request.POST.get("type")) not in ["TDS", "RAPID"]:
        logger.debug(f"Core.calc_fft: Invalid type {data_type}")
        return HttpResponseBadRequest("Invalid parameter")

    present_data = (
        TemporalData.objects.filter(data_type=data_type).order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)

    if (fft := request.POST.get("fft")) not in ["true", "false"]:
        logger.debug(f"Core.calc_fft: Invalid fft type {fft}")
        return HttpResponseBadRequest("Invalid parameter")

    if request.POST.get("fft") == "true":
        if len(wave.x) == 0:
            return JsonResponse({"x": [], "y": []})
        freq, fft = api_ops.calc_fft([wave.x, wave.y])  # (list, list)

        return JsonResponse({"x": freq, "y": fft})
    else:
        return JsonResponse({"x": wave.x, "y": wave.y})


def tds_boot(request) -> JsonResponse:
    """
    Start the sequence of step scanning.
    The endpoint is `core/tds-boot/`

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",

    :returns: Empty JSON
    """
    global tds_running

    present_data = (
        TemporalData.objects.filter(data_type="TDS").order_by("-created_at").first()
    )
    present_data.position_data = ""
    present_data.intensity_data = ""

    try:
        start = int(request.POST.get("start"))
        end = int(request.POST.get("end"))
        step = int(request.POST.get("step"))
        lockin = float(request.POST.get("lockin"))

        logger.debug(f"Core.tds_boot: start = {start}")
        logger.debug(f"Core.tds_boot: end = {end}")
        logger.debug(f"Core.tds_boot: step = {step}")
        logger.debug(f"Core.tds_boot: lockin = {lockin}")
    except (ValueError, TypeError) as e:
        logger.error(f"Core.tds_boot: {e}")
        return HttpResponseBadRequest("Invalid parameter(s)")

    tds_running = True
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
    """
    Get the data of step scanning at the moment.
    The endpoint is `core/tds-data/`

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",

    :returns: JSON data

        - x: The positional data of step motor stage.
        - y: The intensity data of Lockin amplifier.
        - status: Whether the sequence is still running or not.
    """
    present_data = (
        TemporalData.objects.filter(data_type="TDS").order_by("-created_at").first()
    )
    wave = WaveForm.new(present_data)
    status = "running" if tds_running else "finished"
    logger.debug(f"Core.tds_data: status = {status}")

    return JsonResponse({"x": wave.x, "y": wave.y, "status": status})


def change_sensitivity(request) -> HttpResponse:
    """
    Change sensitivity of Lockin amplifier.
    The endpoint is `core/change-sensitivity/`
    If the parameter is invalid, returns 404 Bad Request.

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        - entry:
            - value: The target sensitivity.

    :returns: JSON {"status": "ok"}.

    """
    try:
        value = int(request.POST.get("value"))
        logger.debug(f"Core.change_sensitivity: value = {value}")
    except (ValueError, TypeError) as e:
        logger.error(f"Core.change_sensitivity: {e}")
        return HttpResponseBadRequest("Invalid parameter")

    unit = request.POST.get("unit")
    logger.debug(f"Core.change_sensitivity: unit = {unit}")
    api_ops.set_lockin_sensitivity(value, unit)

    return JsonResponse({"status": "ok"})


def change_time_const(request) -> HttpResponse:
    """
    Change time constant of Lockin amplifier.
    The endpoint is `core/change-time-const/`
    If the parameter is invalid, returns 404 Bad Request.

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        - entry:
            - value: The target time constant.

    :returns: JSON {"status": "ok"}.
    """
    try:
        value = int(request.POST.get("value"))
        logger.debug(f"Core.change_time_const: value = {value}")
    except (ValueError, TypeError) as e:
        logger.error(f"Core.change_time_const: {e}")
        return HttpResponseBadRequest("Invalid parameter")

    unit = request.POST.get("unit")
    logger.debug(f"Core.change_time_const: unit = {unit}")
    api_ops.set_lockin_time_const(value, unit)

    return JsonResponse({"status": "ok"})


def auto_phase(request) -> JsonResponse:
    """
    Auto phase the Lockin amplifier.
    The endpoint is `core/auto-phase/`

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",

    :returns: JSON {"status": "ok"}.
    """
    api_ops.auto_phase_lockin()

    return JsonResponse({"status": "ok"})


def start_rapid_scan(request):
    global scan_running

    scan_running = True
    func = cdll.LoadLibrary("./core/adconverter.dll")

    duration = float(request.POST.get("duration"))
    sample_rate = float(request.POST.get("sampling_rate")) * 1e3
    clk_time = int(1 / sample_rate / 2e-8)

    logger.debug(f"Core.start_rapid_scan: duration = {duration}")
    logger.debug(f"Core.start_rapid_scan: sample_rate = {sample_rate}")
    logger.debug(f"Core.start_rapid_scan: clk_time = {clk_time}")

    func.open(0)
    func.set_clock(0, clk_time, 0)
    func.run(0, int(duration))

    return JsonResponse({"status": "ok"})


def rapid_scan_data(request) -> JsonResponse:
    """
    Receive scanned data from A/D converter
    The endpoint is `core/rapid-scan-data/`

    :param request django.http.HTTPRequest request:

        - "Content-Type": "application/json; charset=utf-8",
        - x: position data
        - y: intensity data
        - finished: bool which represent whether the scan is finished

    :returns: Empty JSON.
    """
    global scan_running

    body = json.loads(request.body)
    present_data = (
        TemporalData.objects.filter(data_type="RAPID").order_by("-created_at").first()
    )
    present_data.position_data = ",".join(map(str, body["x"]))
    present_data.intensity_data = ",".join(map(str, body["y"]))
    present_data.save()

    if body["finished"]:
        func = cdll.LoadLibrary("./core/adconverter.dll")
        func.close(0)
        scan_running = False

    return JsonResponse({})


def send_rapid_data_to_front(request) -> JsonResponse:
    """
    Send scanned data to the frontend to plot data
    The endpoint is `core/get-rapid-data/`

    :param request django.http.HTTPRequest request:

        - "Content-Type":  "application/x-www-form-urlencoded; charset=utf-8"

    :returns: JSON {"running": bool, "x": list[float], "y": list[float]}.
    """
    global scan_running

    data = (
        TemporalData.objects.filter(data_type="RAPID").order_by("-created_at").first()
    )

    try:
        position = list(map(float, data.position_data.split(",")))
        intensity = list(map(float, data.intensity_data.split(",")))

        logger.debug(f"Core:send_rapid_data_to_front: position = {position}")
        logger.debug(f"Core:send_rapid_data_to_front: intensity = {intensity}")

        return JsonResponse({"running": scan_running, "x": position, "y": intensity})
    except ValueError as e:
        logger.error(f"Core.send_rapid_data_to_front: {e}")
        print("send_rapid_data_to_front: ValueError")
        return JsonResponse({"running": scan_running, "x": [], "y": []})
