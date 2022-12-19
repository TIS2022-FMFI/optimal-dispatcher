from django.forms import ModelForm
from django import forms
from .models import UserBranchAccess, Group
from branch_management.models import Branch
from django.core.exceptions import ValidationError
 

class GroupForm(forms.Form):
    # class Meta:
    #     model = Group
    #     fields = ["name"]
    name = forms.CharField(label='Name', max_length=50)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # branch list dropdown
        branch_list = [[i.id, i.name] for i in Branch.objects.all()]
        self.fields['branch'] = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=True)
       


    def clean_name(self):
        group_name = self.cleaned_data['name']
        exists = Group.objects.filter(name=group_name).exists()
        if exists:
            raise ValidationError(('Group with name \"%(value)s\" already exists'), params={'value': group_name})
        return group_name

# class UserBrnachForm(ModelForm):
#     # branch_list = [[i.id, i.name] for i in Branch.objects.all()]
#     # branch = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=False)

#     class Meta:
#         model = UserBranchAccess
#         fields = ['user_id'] #"__all__"

    

# class GroupForm(ModelForm):
#     selected = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    
#     class Meta:
#         model = Group
#         fields = "__all__"
    
#         widgets = {
#             "group_name": forms.TextInput(attrs={"class":"form-control"}),
#             "branch_id": forms.Select(attrs={"class":"form-control","id":"branch","name":"branch"}),
#         }
