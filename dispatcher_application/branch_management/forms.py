from django.forms import ModelForm
from django import forms
from access_management.models import User_branch_access
from user_management.models import MyUser
from .models import Branch
 


class AddBranchAccessForm(forms.ModelForm):

    class Meta:
        model = User_branch_access
        fields = ['user_id', 'branch_id']


    def get_user_without_access(self, branch_id):
        raw_access_table_id = User_branch_access.objects.filter(branch_id=branch_id).values_list('user_id')
        access_users_id = {uid[-1] for uid in set(raw_access_table_id)}

        diff_user_id = MyUser.objects.exclude(id__in=access_users_id).values_list('id', 'email')
        user_list = [u_info for u_info in diff_user_id] 
        user_list.append(['', '---------'])  
        return user_list


    def __init__(self, branch_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch_id'].label = 'Branch'

        # setup branch dropdown values
        branch_obj = Branch.objects.get(id=branch_id)
        self.fields['branch_id'].choices = [[branch_obj.id, branch_obj.name]]
        self.fields['branch_id'].widget.attrs['readonly'] = True
        
        # setup user dropdown values
        self.fields['user_id'].label = 'User'
        user_list = self.get_user_without_access(branch_id)
        self.fields['user_id'].choices = user_list