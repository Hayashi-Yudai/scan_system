from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class Index(View):
    def __init__(self, *args, **kwargs):
        pass

    def get(self, request):
        context = dict()
        return render(request, 'core/index.html', context)
