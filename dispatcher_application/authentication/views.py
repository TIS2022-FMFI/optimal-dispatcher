from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.core import serializers
from django.contrib.auth import views as auth_views

# decorators
from decorators import is_not_authenticated
from django.utils.decorators import method_decorator

from access_management.models import UserBranchAccess, GroupBranchAccess, UserGroupAccess


class CustomLoginView(View):
    template = 'authentication/login.html'

    @method_decorator(is_not_authenticated())
    def get(self, request):
        context = {}
        return render(request, self.template, context)


    @method_decorator(is_not_authenticated())
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            self.setup_user_access()
        
            if user.is_superuser:
                return redirect('user-list')
            return redirect('transportation-list')

        context = {'email' : email, 'error_message' : 'Wrong email or password'}
        return render(request, self.template, context)


    def setup_user_access(self):
        user = self.request.user
        user_branch_access = { user.branch }
        user_branch_access.update({i.branch_id for i in UserBranchAccess.objects.filter(user_id=user.id)})
        groups = {group_access.group_id for group_access in UserGroupAccess.objects.filter(user_id=user.id)}
        user_group_access = {access.branch_id for group in groups for access in GroupBranchAccess.objects.filter(group_id=group)} 
        user_branch_access.update(user_group_access)
        self.request.session['logged_in_user_access'] = serializers.serialize('json', user_branch_access)



decorators = [is_not_authenticated()]

@method_decorator(decorators, name="dispatch")
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name='authentication/reset_password.html'


@method_decorator(decorators, name="dispatch")
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='authentication/reset_password_confirm.html'


@method_decorator(decorators, name="dispatch")
class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='authentication/reset_password_done.html'


@method_decorator(decorators, name="dispatch")    
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='authentication/reset_password_complete.html'



