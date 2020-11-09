from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Ride(models.Model):
    ride_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.DurationField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    average_speed = models.DecimalField(max_digits=5, decimal_places=2)
    calories = models.PositiveSmallIntegerField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

