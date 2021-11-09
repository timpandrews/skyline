from django import forms
from rides.models import Ride
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = (
            'ride_type',
            'ride_native_id',
            'start_time',
            'title',
            'description',
            'duration',
            'distance',
            'elevation',
            'avg_speed',
            'max_speed',
            'avg_heart_rate',
            'max_heart_rate',
            'avg_watts',
            'max_watts',
            'avg_cadence',
            'max_cadence',
            'calories',
            'notes',
        )



