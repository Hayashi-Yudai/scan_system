# from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

from core.models import TDSData

# Create your views here.
class Index(ListView):
    template_name = "archive/index.html"
    model = TDSData
    paginate_by = 2


def get_archive_data(request):
    entry = TDSData.objects.get(pk=int(request.POST.get("pk")))
    x = list(map(float, entry.position_data.split(",")))
    y = list(map(float, entry.intensity_data.split(",")))
    return JsonResponse({"x": x, "y": y})
