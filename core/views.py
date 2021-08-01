from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


class Index(View):
    def __init__(self, *args, **kwargs):
        super(Index, self).__init__(*args, **kwargs)

        self.x = []
        self.y = []

    def get(self, request):
        self.x = [1, 2, 3, 4, 5, 6, 7]
        self.y = [1, 4, 9, 16, 25, 36, 49]

        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/index.html', context)

    def post(self, request):
        context = {"position": self.x, "intensity": self.y}

        return render(request, 'core/index.html', context)

