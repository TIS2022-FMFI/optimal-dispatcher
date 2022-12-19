from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.db import transaction

from django.views.generic.list import ListView
from django.views.generic import CreateView, DeleteView, FormView

from .forms import GroupForm

from .models import Group, GroupBranchAccess
from branch_management.models import Branch

from django.db import IntegrityError


class ListGroupsView(ListView):
    model = Group
    template_name = 'access_management/group_list.html'
    paginate_by = 20


class CreateGroupView(FormView):
    template_name = 'access_management/group_add.html'
    form_class = GroupForm
    success_url = reverse_lazy('group-list')


    def form_valid(self, form):
        form_fields = form.cleaned_data
        
        try:
            with transaction.atomic(): 
                group = Group.objects.create(name=form_fields['name'])
                for b_id in form_fields['branch']:
                    branch = Branch.objects.get(id=b_id)
                    GroupBranchAccess.objects.create(group_id=group, branch_id=branch)
        except IntegrityError:
            ...
        return HttpResponseRedirect(self.get_success_url())



class UpdateGroupView():
    ...


class DeleteGroupView(DeleteView):
    model = Group
    template_name = 'access_management/group_delete.html'
    success_url = reverse_lazy('group-list')


class GroupAccessView():
    ...


class AddGroupAccessView():
    ...


class DeleteGroupAccessView():
    ...



# class ManageUserBranchesView(View):
#     template = 'access_management/add_user_branches.html'


#     def get(self, request):
#         form = UserBrnachForm()
#         context = { 'form':form }
#         return render(request, self.template, context)


#     def post(self, request):
#         user = request.user
#         selected_values = request.POST.getlist('branch')

#         for value in selected_values:
#             UserBranchAccess.objects.create(
#               user_id = user, 
#               branch_id = Branch.objects.get(id=value)
#             )
           

#         form = UserBrnachForm()
#         context = { 'form':form }
#         return render(request, self.template, context)


# class TestTempView(View):
#     template = 'access_management/test_temp.html'
    
#     def get(self, request):
#         user = request.user
#         branches_access = UserBranchAccess.objects.filter(user_id=user.id).values_list('branch_id')
#         branches = Branch.objects.filter(id__in=branches_access)
#         context = { 'user_branches' : branches }
#         print(branches)
#         return render(request, self.template, context)

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




# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import *
# from .forms import *

# def main(request):
#     groups = Groups.objects.all()
    
#     context = {"groups":groups}
    
#     return render(request, "access_management/group_main.html", context)

# def createGroup(request):
#     form = GroupForm()
#     if request.method == "POST":
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("groups")
    
#     context = {"form":form}
#     return render(request, "access_management/group_add.html", context)

# def updateGroup(request,pk):
#     group = Groups.objects.get(id=pk)
#     form = GroupForm(instance=group)
#     if request.method == "POST":
#         form = GroupForm(request.POST,instance=group)
#         if form.is_valid():
#             form.save()
#             return redirect("groups")
    
#     context = {"form":form}
#     return render(request, "access_management/group_add.html", context)


# def deleteGroup(request):
#     groups = Groups.objects.all()
    
#     if request.method == "POST":
#         pole = request.POST.getlist("data")
#         print(pole)
#         for i in pole:
#             obj = Groups.objects.get(id=i)
#             obj.delete()
            
#         return redirect("groups")
            
     
#     context = {"groups":groups}
#     return render(request, "access_management/group_main.html", context)

