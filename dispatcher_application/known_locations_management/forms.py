from django import forms
from .models import Location
from django.core.exceptions import ValidationError
import re


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['zip_code', 'city', 'country']


    # def clean_zip_code(self):
    #     zip_code = self.cleaned_data['zip_code']
    #     return zip_code


    def clean_city(self):
        city = self.cleaned_data['city']
        pattern = r'^[A-Z][a-z]{1,69}$'
        if not(re.match(pattern, city)):
            raise ValidationError(('City must consist of letters and start with capital letter'))
        return city


    def clean_country(self):
        country = self.cleaned_data['country']
        pattern = r'^[A-Z]{2,3}$'
        if not(re.match(pattern, country)):
            raise ValidationError(('Country must consist of capital letters, format(SK, SVK, FR, FRA)'))
        return country