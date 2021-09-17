from django.urls import path

from . import views

app_name = "archive"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("get_archive_data/", views.get_archive_data, name="get_archive_data"),
    path("calc-fft/", views.calc_fft, name="calf_fft"),
]
