from django.forms import ModelForm
from django import forms
from .models import UserBranchAccess, Groups
from branch_management.models import Branch
 



class UserBrnachForm(ModelForm):
    # branch_list = [[i.id, i.name] for i in Branch.objects.all()]
    # branch = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=False)

    class Meta:
        model = UserBranchAccess
        fields = ['user_id'] #"__all__"

    

class GroupForm(ModelForm):
    #selected = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    
    class Meta:
        model = Groups
        fields = "__all__"
    
        widgets = {
            "group_name": forms.TextInput(attrs={"class":"form-control"}),
            "branch_id": forms.Select(attrs={"class":"form-control","id":"branch","name":"branch"}),
        }
