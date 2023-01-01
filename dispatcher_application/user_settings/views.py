from django.shortcuts import render, redirect


from django.views.generic import View
from .forms import ChangePasswordForm
from access_management.models import UserBranchAccess, UserGroupAccess, GroupBranchAccess


### change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decorators = [login_required()]

@method_decorator(decorators, name="dispatch")
class UserSettingsView(View):
    template = 'user_settings/profile_settings.html'

    def get(self, request):
        user = request.user
        branch_access = { request.user.branch }
        branch_access.update({i.branch_id for i in UserBranchAccess.objects.filter(user_id=user.id)})
        groups = {group_access.group_id for group_access in UserGroupAccess.objects.filter(user_id=user.id)}
        user_group_access = {access.branch_id for group in groups for access in GroupBranchAccess.objects.filter(group_id=group)} 
        branch_access.update(user_group_access)

        context = { 
            'email' : user.email,
            'first_name' : user.first_name ,
            'last_name' : user.last_name,
            'branch' : user.branch,
            'access_list' : branch_access,
        }
        return render(request, self.template, context)


@method_decorator(decorators, name="dispatch")
class ChangePasswordView(View):
    template = 'user_settings/profile_password_change.html'

    def get(self, request):
        form = ChangePasswordForm(request.user)
        context = { 'form' : form }
        return render(request, self.template, context)

    
    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed')
            return redirect('user-settings')
        
        messages.error(request, 'Old password is invalid or new password does not meet requirements')
        form = ChangePasswordForm(request.user)
        context = { 'form' : form }
        return render(request, self.template, context) 

