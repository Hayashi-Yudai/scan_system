from django.views.generic import ListView
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import numpy as np
import json
import logging

from core.models import TDSData
from core.utils import waveform


logger = logging.getLogger("root")


class Index(ListView):
    template_name = "archive/index.html"
    model = TDSData
    ordering = ["-measured_date"]
    paginate_by = 8


def get_archive_data(request):
    try:
        entry = TDSData.objects.get(pk=int(request.POST.get("pk")))
    except ObjectDoesNotExist as e:
        logger.error(f"archive.get_archive_data: {e}")
        raise Http404("Resource not found")
    except (ValueError, TypeError) as e:
        logger.error(f"archive.get_archive_data: {e}")
        return HttpResponseBadRequest("Invalid parameter(s)")

    wave = waveform.WaveForm.new(entry)
    if entry.start_position is None:
        wave.transform()
    x = wave.x
    y = wave.y

    if request.POST.get("fft") == "true":
        delta_time = (x[1] - x[0]) * 1e-6 * 2 / 2.9979e8
        freq = [i / delta_time / 4096 for i in range(4096)]
        y_fft = abs(np.fft.fft(y, 4096)).tolist()

        return JsonResponse({"x": freq, "y": y_fft})
    elif request.POST.get("fft") == "false":
        return JsonResponse({"x": x, "y": y})
    else:
        return HttpResponseBadRequest("Invalid parameter(s)")


def calc_fft(request):
    body = json.loads(request.body)
    xs = []
    ys = []
    try:
        ids = body["ids"]
        fft = body["fft"]
        logger.debug(f"archive.calc_fft: ids = {ids}")
        logger.debug(f"archive.calc_fft: fft = {fft}")
    except KeyError as e:
        logger.error(f"archive.calc_fft: {e}")
        return HttpResponseBadRequest("Invalid parameter")

    if not type(ids) == list and not type(ids) == tuple:
        return HttpResponseBadRequest("Invalid parameter")

    for pk in ids:
        try:
            data = TDSData.objects.filter(pk=pk)[0]
        except IndexError as e:
            logger.error(f"archive.calc_fft: {e}")
            raise Http404("Resource not found")

        wave = waveform.WaveForm.new(data)
        if data.start_position is None:
            wave.transform()
        x = wave.x
        y = wave.y

        if fft is True:
            if data.step is not None:
                delta_time = data.step * 1e-6 * 2 / 2.9979e8
            else:
                delta_time = 6e-6 * 2 / 2.9979e8
            freq = [i / delta_time / 4096 for i in range(4096)]

            xs.append(freq)
            ys.append(abs(np.fft.fft(y, 4096)).tolist())
        elif fft is False:
            xs.append(x)
            ys.append(y)
        else:
            return HttpResponseBadRequest("Invalid parameter")

    return JsonResponse({"xs": xs, "ys": ys})


def download_data(request):
    body = json.loads(request.body)
    data = TDSData.objects.get(pk=int(body["pk"]))
    wave = waveform.WaveForm.new(data)
    if data.start_position is None:
        wave.transform()

    filename = data.file_name if data.file_name else "Untitled"
    csv_data = pd.DataFrame({"position": wave.x, "intensity": wave.y})
    csv_data.to_csv(f"~/Downloads/{filename}.csv")

    return JsonResponse({})


def delete_data(request):
    body = json.loads(request.body)
    data = TDSData.objects.get(pk=int(body["pk"]))
    data.delete()

    return JsonResponse({})
