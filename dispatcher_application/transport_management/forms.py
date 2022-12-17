from django.forms import ModelForm
from django import forms
from .models import *

class TransportForm(ModelForm):
    class Meta:
        model = Transportations
        fields = "__all__"
        exclude = ["owner_id"]
    
    widgets = {
            "from_id": forms.Select(attrs={"class":"form-control","label":"From: "}),
            "to_id": forms.Select(attrs={"class":"form-control","label":"To: "}),
            "departure_time": forms.DateTimeField(input_formats=['%d-%m-%y %H:%M']),
            "ldm": forms.NumberInput(attrs={"class":"form-control","label":"L(m): "}),
            "weight": forms.NumberInput(attrs={"class":"form-control","label":"Weight: "}),
            "info": forms.Textarea(attrs={"class":"form-control","label":"Info: "}),
        }