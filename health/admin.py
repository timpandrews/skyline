from django.contrib import admin

from health.models import Health


@admin.register(Health)
class HealthAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'health_type',
        'health_value1',
        'health_value2',
        'health_date',
        'user_id'
    )
    ordering = ('-id',)
