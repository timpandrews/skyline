from django import forms
from data.models import Ride

class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = (
            'ride_date',
            'title',
            'description',
            'duration',
            'distance',
            'average_speed',
            'calories',
            'notes'
        )