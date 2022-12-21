from django.forms import ModelForm
from django import forms
from .models import GroupBranchAccess, Group
from branch_management.models import Branch
from django.core.exceptions import ValidationError
 

class GroupAddForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # branch list dropdown
        branch_list = [[i.id, i.name] for i in Branch.objects.all()]
        self.fields['branch'] = forms.MultipleChoiceField(choices=branch_list,widget=forms.SelectMultiple(), required=True) # CheckboxSelectMultiple
       

    def clean_name(self):
        group_name = self.cleaned_data['name']
        exists = Group.objects.filter(name=group_name).exists()
        if exists:
            raise ValidationError(('Group with name \"%(value)s\" already exists'), params={'value': group_name})
        return group_name


class GroupUpdateForm(GroupAddForm):

    def __init__(self, g_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.group_obj = Group.objects.get(id=g_id)
        self.fields['name'].initial = self.group_obj.name

        group_access_branch_list = GroupBranchAccess.objects.filter(group_id=g_id).values_list('branch_id', flat=True)
        self.fields['branch'].initial = [i for i in group_access_branch_list]

    
    def clean_name(self):
        group_name = self.cleaned_data['name']
        exists = Group.objects.filter(name=group_name).exclude(name=self.group_obj.name).exists()
        if exists:
            raise ValidationError(('Group with name \"%(value)s\" already exists'), params={'value': group_name})
        return group_name


