# from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
import numpy as np
import json
import logging

from core.models import TDSData


logger = logging.getLogger("root")


class Index(ListView):
    template_name = "archive/index.html"
    model = TDSData
    ordering = ["-measured_date"]
    paginate_by = 10


def get_archive_data(request):
    try:
        entry = TDSData.objects.get(pk=int(request.POST.get("pk")))
    except ObjectDoesNotExist as e:
        logger.error(f"archive.get_archive_data: {e}")
        raise Http404("Resource not found")
    except (ValueError, TypeError) as e:
        logger.error(f"archive.get_archive_data: {e}")
        return HttpResponseBadRequest("Invalid parameter(s)")

    x = list(map(float, entry.position_data.split(",")))
    y = list(map(float, entry.intensity_data.split(",")))

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

        x = list(map(float, data.position_data.split(",")))
        y = list(map(float, data.intensity_data.split(",")))

        if fft is True:
            delta_time = data.step * 1e-6 * 2 / 2.9979e8
            freq = [i / delta_time / 4096 for i in range(4096)]

            xs.append(freq)
            ys.append(abs(np.fft.fft(y, 4096)).tolist())
        elif fft is False:
            xs.append(x)
            ys.append(y)
        else:
            return HttpResponseBadRequest("Invalid parameter")

    return JsonResponse({"xs": xs, "ys": ys})
