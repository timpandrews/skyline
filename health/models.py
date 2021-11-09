from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

class Health(models.Model):
    HEALTH_TYPE = (
        ('weight', 'weight'),
        ('bp', 'bp'),
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
    )
    health_type = models.CharField(max_length=25, choices=HEALTH_TYPE,)
    health_value1 = models.IntegerField(blank=True)
    health_value2 = models.IntegerField(blank=True)
    health_date = models.DateTimeField()
    health_notes = models.TextField(blank=True)

    def __str__(self):
        return  self.health_type
