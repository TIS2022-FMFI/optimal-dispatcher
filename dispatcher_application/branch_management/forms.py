from django import forms
from django.db.models import Q
from access_management.models import UserBranchAccess
from user_management.models import MyUser
from .models import Branch
from django.core.exceptions import ValidationError
import re
 


class AddBranchAccessForm(forms.ModelForm):

    class Meta:
        model = UserBranchAccess
        fields = ['user_id', 'branch_id']


    def get_user_without_access(self, branch_id):
        raw_access_table_id = UserBranchAccess.objects.filter(branch_id=branch_id).values_list('user_id')
        access_users_id = {uid[-1] for uid in set(raw_access_table_id)}

        diff_user_id = MyUser.objects.exclude(Q(id__in=access_users_id) | Q(branch_id=branch_id)).values_list('id', 'email')
        user_list = [u_info for u_info in diff_user_id] 
        choice_list = [['', '---------']]
        choice_list.extend(user_list)
        return choice_list


    def __init__(self, branch_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch_id'].label = 'Branch'

        # setup branch dropdown values
        branch_obj = Branch.objects.get(id=branch_id)
        self.fields['branch_id'].choices = [[branch_obj.id, branch_obj.name]]
        
        # setup user dropdown values
        self.fields['user_id'].label = 'User'
        user_list = self.get_user_without_access(branch_id)
        self.fields['user_id'].choices = user_list



class AddBranch(forms.ModelForm):

    class Meta:
        model = Branch
        fields = [ 'name' ]


    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) > 70:
            raise ValidationError("Maximum length is 70 characters.")
        
        if len(name) < 4:
            raise ValidationError("Minimum length is 4 characters.")

        pattern = r'^[a-zA-Z0-9_ -]{4,70}$'
        if not(re.match(pattern, name)):
            raise ValidationError("Invalid format, allowed alphanumeric characters, space and _- characters.")
        return name
