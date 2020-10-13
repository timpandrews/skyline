from django.contrib import admin

from data.models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id','ride_date','title','duration','distance')
    ordering = ('-ride_date', 'id')
