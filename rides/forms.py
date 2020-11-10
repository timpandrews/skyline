from django import forms
from rides.models import Ride

class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = (
            'start_time',
            'title',
            'description',
            'duration',
            'distance',
            'avg_speed',
            'calories',
            'notes'
        )
