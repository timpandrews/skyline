from django.contrib import admin

from rides.models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'start_time',
        'description',
        'duration',
        'distance',
        'avg_speed',
        'calories'
    )
    ordering = ('-id',)
