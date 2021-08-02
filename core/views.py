from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import os
import pandas as pd

from core.waveform import WaveForm

wave = WaveForm()


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

        return render(request, 'core/index.html', context)

    def post(self, request):
        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/index.html', context)


def move(request):
    position = int(request.POST.get("position"))
    return JsonResponse({"position": position + 1})
