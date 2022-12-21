from django.shortcuts import render, redirect


from django.views.generic import View
from .forms import ChangePasswordForm
from access_management.models import UserBranchAccess, UserGroupAccess


### change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


class UserSettingsView(View):
    template = 'user_settings/profile_settings.html'

    def get(self, request):
        logged_user = request.user
        branch_access = [i.branch_id for i in UserBranchAccess.objects.filter(user_id=logged_user.id)]

        context = { 
            'email' : logged_user.email,
            'first_name' : logged_user.first_name ,
            'last_name' : logged_user.last_name,
            'branch' : logged_user.branch,
            'access_list' : branch_access,
        }
        return render(request, self.template, context)


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

