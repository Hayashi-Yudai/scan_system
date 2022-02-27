from django.db import models


class TDSData(models.Model):
    class Meta:
        app_label = "core"

    measured_date = models.DateTimeField(auto_now_add=True)
    # step scanning information
    start_position = models.PositiveIntegerField(null=True)
    end_position = models.PositiveIntegerField(null=True)
    step = models.PositiveIntegerField(null=True)
    lockin_time = models.PositiveIntegerField(null=True)
    # rapid scan information
    sampling_rate = models.FloatField(null=True)  # kHz
    measuring_time = models.FloatField(null=True)  # sec
    # common information
    measure_type = models.CharField(max_length=10, default="RAPID")
    position_data = models.TextField(blank=False)
    intensity_data = models.TextField(blank=False)
    file_name = models.TextField(blank=True)


class TemporalData(models.Model):
    class Meta:
        app_label = "core"

    created_at = models.DateTimeField(auto_now_add=True)
    data_type = models.TextField(blank=False)  # "RAPID" or "TDS"
    position_data = models.TextField(blank=True)
    intensity_data = models.TextField(blank=True)
