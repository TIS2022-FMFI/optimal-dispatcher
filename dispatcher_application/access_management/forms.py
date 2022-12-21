from django.forms import ModelForm
from django import forms
from .models import GroupBranchAccess, Group
from branch_management.models import Branch
from django.core.exceptions import ValidationError
from access_management.models import UserGroupAccess
from user_management.models import MyUser
from django.db.models import Q
 

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



class AddGroupAccessForm(forms.ModelForm):

    class Meta:
        model = UserGroupAccess
        fields = ['user_id', 'group_id']


    def get_user_without_access(self, g_id):
        raw_access_table_id = UserGroupAccess.objects.filter(group_id=g_id).values_list('user_id')
        access_users_id = {uid[-1] for uid in set(raw_access_table_id)}

        diff_user_id = MyUser.objects.exclude(id__in=access_users_id).values_list('id', 'email')
        user_list = [u_info for u_info in diff_user_id] 
        choice_list = [['', '---------']]
        choice_list.extend(user_list)
        return choice_list


    def __init__(self, group_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_id'].label = 'Group'

        # setup branch dropdown values
        group_obj = Group.objects.get(id=group_id)
        self.fields['group_id'].choices = [[group_obj.id, group_obj.name]]
        
        # setup user dropdown values
        self.fields['user_id'].label = 'User'
        user_list = self.get_user_without_access(group_id)
        self.fields['user_id'].choices = user_list

