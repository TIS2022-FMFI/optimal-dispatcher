from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from transport_management.models import Transportations
import re


class CreateTransportForm(forms.ModelForm):
    class Meta:
        model = Transportations
        fields = [
            'departure_time', 'arrival_time', 'ldm', 'weight', 'info'
        ]
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['from_id'] = forms.CharField(label='From', max_length=50)
        self.fields['from_id'].widget.attrs.update({'list': "from_locations"})

        self.fields['to_id'] = forms.CharField(label='To', max_length=50)
        self.fields['to_id'].widget.attrs.update({'list': "to_locations"})

        self.fields['info'].required = False

    def location_check(self, location_type):
        location_input = str(self.cleaned_data[location_type]).strip()
        pattern = r'([0-9]{5,10})[ ,/.]([A-Z][a-z]{1,69})[ ,/.]([A-Z]{2,4})'
        if not re.match(pattern, location_input):
            raise ValidationError('Wrong location input.')
        return self.cleaned_data[location_type]

    def clean_to_id(self):
        return self.location_check('to_id')

    def clean_from_id(self):
        return self.location_check('from_id')

    def clean_departure_time(self):
        return self.cleaned_data['departure_time']

    def clean_arrival_time(self):
        if not (self.cleaned_data['departure_time'] < self.cleaned_data['arrival_time']):
            raise ValidationError('Departure time must be before arrival time.')
        return self.cleaned_data['arrival_time']

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


class UpdateTransportForm(CreateTransportForm):
    def __init__(self, t_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            transportation = Transportations.objects.get(id=t_id)
        except Transportations.DoesNotExist:
            raise Http404

        self.fields['from_id'].initial = transportation.from_id
        self.fields['to_id'].initial = transportation.to_id
        self.fields['departure_time'].initial = transportation.departure_time
        self.fields['arrival_time'].initial = transportation.arrival_time
        self.fields['ldm'].initial = transportation.ldm
        self.fields['weight'].initial = transportation.weight
        self.fields['info'].initial = transportation.info
