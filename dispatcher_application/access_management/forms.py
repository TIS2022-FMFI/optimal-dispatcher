from django.forms import ModelForm
from django import forms
from .models import UserBranchAccess
from branch_management.models import Branch
 



class UserBrnachForm(ModelForm):
    # branch_list = [[i.id, i.name] for i in Branch.objects.all()]
    # branch = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=False)

    class Meta:
        model = UserBranchAccess
        fields = ['user_id'] #"__all__"

    
    