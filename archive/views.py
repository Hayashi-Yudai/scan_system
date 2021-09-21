# from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
import numpy as np
import json

from core.models import TDSData


# Create your views here.
class Index(ListView):
    template_name = "archive/index.html"
    model = TDSData
    ordering = ["-measured_date"]
    paginate_by = 20


def get_archive_data(request):
    entry = TDSData.objects.get(pk=int(request.POST.get("pk")))
    x = list(map(float, entry.position_data.split(",")))
    y = list(map(float, entry.intensity_data.split(",")))

    if request.POST.get("fft") == "true":
        delta_time = (x[1] - x[0]) * 1e-6 * 2 / 2.9979e8
        freq = [i / delta_time / 4096 for i in range(4096)]
        y_fft = abs(np.fft.fft(y, 4096)).tolist()

        return JsonResponse({"x": freq, "y": y_fft})
    else:
        return JsonResponse({"x": x, "y": y})


def calc_fft(request):
    body = json.loads(request.body)
    xs = []
    ys = []
    for pk in body["ids"]:
        data = TDSData.objects.filter(pk=pk)[0]
        x = list(map(float, data.position_data.split(",")))
        y = list(map(float, data.intensity_data.split(",")))

        if body["fft"]:
            delta_time = data.step * 1e-6 * 2 / 2.9979e8
            freq = [i / delta_time / 4096 for i in range(4096)]

            xs.append(freq)
            ys.append(abs(np.fft.fft(y, 4096)).tolist())
        else:
            xs.append(x)
            ys.append(y)

    return JsonResponse({"xs": xs, "ys": ys})
