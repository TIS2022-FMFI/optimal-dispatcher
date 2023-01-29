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
        self.fields['from_id'].widget.attrs.update({'list' : "from_locations"})
        self.fields['from_id'].widget.attrs.update({'placeholder' : 'zip code,city,country'})

        self.fields['to_id'] = forms.CharField(label='To', max_length=50)
        self.fields['to_id'].widget.attrs.update({'list' : "to_locations"})
        self.fields['to_id'].widget.attrs.update({'placeholder' : 'zip code,city,country'})

        self.fields['info'].required = False
        self.fields['info'].widget.attrs.update({'placeholder' : 'Add information about transportation'})

        self.fields['ldm'].widget.attrs.update({'placeholder' : '0-100', 'min' : '0', 'max' : '100'})
        self.fields['weight'].widget.attrs.update({'placeholder' : '0-100 000', 'min' : '0', 'max' : '100000'})
     


    def location_check(self, location_type):
        location_input = str(self.cleaned_data[location_type]).strip()
        pattern = r'([0-9]{5,10}),([A-Z][a-z]{1,69}),([A-Z]{2,4})'
        if not re.match(pattern, location_input):
            raise ValidationError('Invalid format, expected: zip code,city,country code.')
        return self.cleaned_data[location_type]

    
    def check_info(self, info):
        pattern = r'^[a-zA-Z0-9._ @-]*$'
        if not re.match(pattern, info):
            raise ValidationError(
                    'Invalid format, allowed only alphanumeric characters, space and .@-_ characters.'\
                )
        return info


    def clean_to_id(self):
        return self.location_check('to_id')


    def clean_from_id(self):
        return self.location_check('from_id')


    def clean_departure_time(self):
        return self.cleaned_data['departure_time']


    def clean_arrival_time(self):
        if not (self.cleaned_data['departure_time'] < self.cleaned_data['arrival_time']):
            raise ValidationError('Date must be after departure time.')
        return self.cleaned_data['arrival_time']


    def clean_ldm(self):
        ldm = self.cleaned_data['ldm']
        if not (0 < ldm <= 100):
            raise ValidationError('Value must be between 0 and 100.')
        return ldm


    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if not (0 < weight <= 100000):
            raise ValidationError('Value must be between 0 and 100 000.')
        return weight


    def clean_info(self):
        return self.check_info(self.cleaned_data['info'].strip())


class UpdateTransportForm(CreateTransportForm):

    def __init__(self, transportation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['from_id'].initial = transportation.from_id
        self.fields['to_id'].initial = transportation.to_id
        self.fields['departure_time'].initial = transportation.departure_time
        self.fields['arrival_time'].initial = transportation.arrival_time
        self.fields['ldm'].initial = transportation.ldm
        self.fields['weight'].initial = transportation.weight
        self.fields['info'].initial = transportation.info
