from django import forms
import re

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import MyUser
from django.core.exceptions import ValidationError



class CreateRegistrationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'email', 'branch', 'password1', 'password2', 'is_superuser',
        ]

        help_texts = {
            'password' : None,
        }

    
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['password1'].help_text=''
      self.fields['password2'].help_text=''


    def name_check(self, name_type):
        name = self.cleaned_data[name_type].strip()

        if len(name) == 0:
            raise ValidationError('Your name can not be empty')

        if not(name.isalpha()):
            raise ValidationError('Your name must contain only alphabet characters')

        data = name[0].upper() + name[1:]
        return data


    def clean_first_name(self):
        return self.name_check('first_name')

    
    def clean_last_name(self):
        return self.name_check('last_name')


    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        email_matcher = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not(re.fullmatch(email_matcher, email)):
            raise ValidationError("Email is invalid")
        return email
        # first_part_of_email, second_part_of_email = email.split('@')
        # valid_email_providers = ['gefco.net']

        # if second_part_of_email not in valid_email_providers:
        #     providers_string = ', '.join([f'@{provider}' for provider in valid_email_providers])
        #     raise ValidationError(f'Email is invalid. Valid email endings {providers_string}')
                
        # if not(first_part_of_email.isalnum()):
        #     raise ValidationError("Email is invalid")
        # return email




class CustomUserChangeForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'branch', 'is_active'
        ]






    