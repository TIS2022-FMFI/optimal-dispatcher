from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .models import User_branch_access
from branch_management.models import Branch

from .forms import UserBrnachForm


class ManageUserBranchesView(View):
    template = 'access_management/add_user_branches.html'


    def get(self, request):
        form = UserBrnachForm()
        context = { 'form':form }
        return render(request, self.template, context)


    def post(self, request):
        user = request.user
        selected_values = request.POST.getlist('branch')

        for value in selected_values:
            User_branch_access.objects.create(
              user_id = user, 
              branch_id = Branch.objects.get(id=value)
            )
           

        form = UserBrnachForm()
        context = { 'form':form }
        return render(request, self.template, context)


class TestTempView(View):
    template = 'access_management/test_temp.html'
    
    def get(self, request):
        user = request.user
        branches_access = User_branch_access.objects.filter(user_id=user.id).values_list('branch_id')
        branches = Branch.objects.filter(id__in=branches_access)
        context = { 'user_branches' : branches }
        print(branches)
        return render(request, self.template, context)

#  if request.method == "POST":
#         form = ChangePasswordForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password have been successfully changed')
#             return redirect('change-password')
#         else:
#             messages.error(request, 'Old password is invalid or new password does not meet requirements')
#     form = ChangePasswordForm(request.user)
#     context = {'form':form}
#     return render(request, 'notesApp/change_password.html', context)



# class LoginView(View):
#     template = 'authentication/login.html'

#     @method_decorator(is_not_authenticated())
#     def get(self, request):
#         context = {}
#         return render(request, self.template, context)


#     @method_decorator(is_not_authenticated())
#     def post(self, request):
#         email = request.POST['email']
#         password = request.POST['password']

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 return redirect('/admin-panel/create-user')
#             return redirect('/transports')

#         context = {'email' : email, 'error_message' : 'Wrong email or password'}
#         return render(request, self.template, context)



