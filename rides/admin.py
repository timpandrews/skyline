from django.contrib import admin

from rides.models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_time',
        'title',
        'description',
        'duration',
        'distance',
        'avg_speed',
        'calories'
    )
    ordering = ('-id',)
