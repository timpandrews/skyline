from django import forms
from health.models import Health
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class HealthForm(forms.ModelForm):
    health_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Health
        fields = (
            'health_type',
            'health_value1',
            'health_value2',
            'health_date',
            'health_notes'
        )