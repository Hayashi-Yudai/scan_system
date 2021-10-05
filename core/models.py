from django.db import models


class TDSData(models.Model):
    class Meta:
        app_label = "core"

    measured_date = models.DateTimeField(auto_now_add=True)
    start_position = models.PositiveIntegerField()
    end_position = models.PositiveIntegerField()
    step = models.PositiveIntegerField()
    lockin_time = models.PositiveIntegerField()
    position_data = models.TextField(blank=False)
    intensity_data = models.TextField(blank=False)
    file_name = models.TextField(blank=True)


class TemporalData(models.Model):
    class Meta:
        app_label = "core"

    created_at = models.DateTimeField(auto_now_add=True)
    data_type = models.TextField(blank=False)
    position_data = models.TextField(blank=True)
    intensity_data = models.TextField(blank=True)
