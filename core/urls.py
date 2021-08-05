from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("tds/", views.TDS.as_view(), name="tds"),
    path("move/", views.move, name="move"),
    path("save/", views.save, name="save"),
    path("scan/", views.scan, name="scan"),
    path("gpib/", views.gpib, name="gpib"),
    path("calc-fft/", views.calc_fft, name="calc_fft"),
    path("tds-data/", views.tds_data, name="tds_data"),
    path("tds-boot/", views.tds_boot, name="tds_boot"),
]
