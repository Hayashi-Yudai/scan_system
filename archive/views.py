# from django.shortcuts import render
from django.views.generic import ListView

from core.models import TDSData

# Create your views here.
class Index(ListView):
    template_name = "archive/index.html"
    model = TDSData
    paginate_by = 2

