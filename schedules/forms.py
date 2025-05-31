from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["start_location", "destination", "arrival_time", "departure_time", "day_available"]
        widgets = {
            "arrival_time": forms.TimeInput(attrs={"type": "time"}),
            "departure_time": forms.TimeInput(attrs={"type": "time"}),
        }
