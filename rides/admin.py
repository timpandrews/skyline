from django.contrib import admin

from rides.models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ride_date',
        'title',
        'description',
        'duration',
        'distance',
        'average_speed',
        'calories'
    )
    ordering = ('-ride_date', 'id')
