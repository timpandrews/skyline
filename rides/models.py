from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Ride(models.Model):
    ride_type = models.CharField(max_length=10)
    ride_native_id = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.DurationField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    elevation = models.IntegerField()
    avg_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    max_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    avg_heart_rate = models.IntegerField(blank=True)
    max_heart_rate = models.IntegerField(blank=True)
    avg_watts = models.IntegerField(blank=True)
    max_watts = models.IntegerField(blank=True)
    avg_cadence = models.IntegerField(blank=True)
    max_cadence = models.IntegerField(blank=True)
    calories = models.PositiveSmallIntegerField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

