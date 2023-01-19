from django import forms
from django.core.exceptions import ValidationError

from transport_management.models import Transportations
import re


class ManageTransportForm(forms.ModelForm):
    class Meta:
        model = Transportations
        fields = [
            'from_id', 'to_id', 'departure_time', 'arrival_time', 'ldm', 'weight', 'info'
        ]
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def location_check(self, location_type):


        location_input = str(self.cleaned_data[location_type]).strip()
        pattern = r'([0-9]{5,10})[ ,/.]([A-Z][a-z]{1,69})[ ,/.]([A-Z]{2,4})'

        if not re.match(pattern, location_input):
            raise ValidationError('Invalid format.')
        return self.cleaned_data[location_type]

    def clean_to_id(self):
        return self.location_check('to_id')

    def clean_from_id(self):
        return self.location_check('from_id')

    def clean_arrival_time(self):
        return self.cleaned_data['arrival_time']

    def clean_departure_time(self):
        return self.cleaned_data['departure_time']

    def clean_ldm(self):
        ldm = self.cleaned_data['ldm']
        if not (0 < ldm <= 13.6):
            raise ValidationError('Invalid value.')

        return ldm

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if not (0 < weight <= 24000):
            raise ValidationError('Invalid value.')

        return weight

    def clean_info(self):
        info = self.cleaned_data['info'].strip()
        return info

