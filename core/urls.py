from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.RapidScan.as_view(), name="rapid"),
    path("step/", views.StepScan.as_view(), name="step"),
    path("move/", views.move, name="move"),
    path("save/", views.save, name="save"),
    path("start_rapid_scan/", views.start_rapid_scan, name="start"),
    path("gpib/", views.gpib, name="gpib"),
    path("calc-fft/", views.calc_fft, name="calc_fft"),
    path("tds-data/", views.tds_data, name="tds_data"),
    path("tds-boot/", views.tds_boot, name="tds_boot"),
    path("change-sensitivity/", views.change_sensitivity, name="change_sensitivity"),
    path("change-time-const/", views.change_time_const, name="change_time_const"),
    path("auto-phase/", views.auto_phase, name="auto_phase"),
    path("rapid-scan-data/", views.rapid_scan_data, name="rapid_scan_data"),
    path("get-rapid-data/", views.send_rapid_data_to_front, name="get_rapid_data"),
]
