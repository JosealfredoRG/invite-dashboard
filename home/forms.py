from django import forms
from .models import Event, Guest

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_date',
            'ceremony_location',
            'reception_location',
            'ceremony_map_location',
            'reception_map_location',
            'groom_name',
            'bride_name',
            'observations'
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
