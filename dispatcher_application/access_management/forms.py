
# from ..branch_management.models import Branch

from django.forms import ModelForm
from django import forms
from .models import User_branch_access
from branch_management.models import Branch
 



class UserBrnachForm(ModelForm):
    branch_list = [[i.id, i.name] for i in Branch.objects.all()]
    # print(branch_list)
    branch = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=False)

    class Meta:
        model = User_branch_access
        fields = ['user_id'] #"__all__"

    

# LINEITEM_CHOICES = [[x.id, x.descr] for x in LineItems.objects.all()]

# class LineItemsForm(forms.Form):
#     food = forms.MultipleChoiceField(choices=LINEITEM_CHOICES,
#     widget=forms.CheckboxSelectMultiple(), required=False)
    