from django import forms
from .models import Location
from django.core.exceptions import ValidationError
import re


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['zip_code', 'city', 'country']


    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        pattern = r'^[0-9A-Za-z- _]{4,13}$'
        if not(re.match(pattern, zip_code)):
            raise ValidationError('Invalid format, allowed alphanumeric characters, space, - and _.')
        return zip_code


    def clean_city(self):
        city = self.cleaned_data['city']
        pattern = r'^[A-Z][a-z]{1,69}$'
        if not(re.match(pattern, city)):
            raise ValidationError('Invalid format, allowed alphabet characters, must start with capital letter.')
        return city


    def clean_country(self):
        country = self.cleaned_data['country']
        pattern = r'^[A-Z]{2,3}$'
        if not(re.match(pattern, country)):
            raise ValidationError('Invalid format, allowed capital letters, format(SK, SVK, FR, FRA).')
        return country
