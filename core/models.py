from django.db import models


# Create your models here.
class TDSData(models.Model):
    measured_date = models.DateTimeField(auto_now_add=True)
    start_position = models.PositiveIntegerField()
    end_position = models.PositiveIntegerField()
    step = models.PositiveIntegerField()
    lockin_time = models.PositiveIntegerField()
    position_data = models.TextField(blank=False)
    intensity_data = models.TextField(blank=False)
    file_name = models.TextField(blank=True)
