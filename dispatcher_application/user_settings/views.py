from django.shortcuts import render, redirect


from django.views.generic import View
from .forms import ChangePasswordForm
from django.core import serializers

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
        user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access']) }

        context = { 
            'email' : user.email,
            'first_name' : user.first_name ,
            'last_name' : user.last_name,
            'branch' : user.branch,
            'access_list' : user_branch_access,
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
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('user-settings')
        
        messages.error(request, 'Old password is invalid or new password does not meet requirements.')
        form = ChangePasswordForm(request.user)
        context = { 'form' : form }
        return render(request, self.template, context) 

