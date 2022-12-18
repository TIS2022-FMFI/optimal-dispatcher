from django.forms import ModelForm
from django import forms
from .models import *

class GroupForm(ModelForm):
    selected = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    
    class Meta:
        model = Groups
        fields = "__all__"
    
        widgets = {
            "group_name": forms.TextInput(attrs={"class":"form-control"}),
            "branch_id": forms.Select(attrs={"class":"form-control","id":"branch","name":"branch"}),
        }