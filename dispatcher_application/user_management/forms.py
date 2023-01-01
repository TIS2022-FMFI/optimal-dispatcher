from django import forms
import re

from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.core.exceptions import ValidationError


class GeneralUserForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'branch'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def name_check(self, name_type):
        name = self.cleaned_data[name_type].strip()

        if len(name) > 70:
            raise ValidationError("Maximum length is 70 characters.")

        if len(name) < 2:
            raise ValidationError('Minimum length is 2 characters.')

        pattern = r'^[A-Z][a-z]{1,69}$'
        if not(re.match(pattern, name)):
            raise ValidationError('Invalid format, allowed alphabet characters, must start with capital letter.')

        return name

    
    def clean_first_name(self):
        return self.name_check('first_name')

    
    def clean_last_name(self):
        return self.name_check('last_name')


class CustomUserCreateForm(UserCreationForm, GeneralUserForm):

    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'email', 'branch', 'password1', 'password2', 'is_superuser',
        ]

     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if len(email) > 60:
            raise ValidationError("Maximum length is 60 characters.")

        pattern = r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not(re.match(pattern, email)):
            raise ValidationError("Invalid format, allowed alphanumeric characters and .-_@ characters.")
        return email



class CustomUserUpdateForm(GeneralUserForm):

    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'branch', 'is_active'
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



