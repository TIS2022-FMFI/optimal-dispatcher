from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

# view imports
from django.views.generic.list import ListView
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from .models import MyUser
from access_management.models import UserBranchAccess, UserGroupAccess, Group
from branch_management.models import Branch
from .forms import CustomUserCreateForm, CustomUserUpdateForm

# decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decorators import admin_permission
decorators = [login_required(), admin_permission()]


@method_decorator(decorators, name="dispatch")
class ListAllUsersView(ListView):
    model = MyUser
    template_name = 'user_management/user_list.html'
    paginate_by = 25

    def get_queryset(self): 
        search_value = self.request.GET.get('search-box')
        self.filtered_by = ''
        self.search_val = ''
        if search_value is None or search_value.strip() == '':
           return MyUser.objects.all()

        self.search_val = search_value
        self.filtered_by = f'&search-box={search_value}'
        result = MyUser.objects.annotate(
            search=SearchVector('email'),
            ).filter(search=search_value)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
        return context
    

@method_decorator(decorators, name="dispatch")
class RegisterNewUserView(CreateView):
    model = MyUser
    template_name = 'user_management/user_add.html'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('user-list')


@method_decorator(decorators, name="dispatch")
class UpdateUserView(UpdateView):
    model = MyUser
    template_name = 'user_management/user_update.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('user-list')


@method_decorator(decorators, name="dispatch")
class DeleteUserView(DeleteView):
    model = MyUser
    template_name = 'user_management/user_delete.html'
    success_url = reverse_lazy('user-list')


class UserDetailView(DetailView):
    model = MyUser
    template_name = 'user_management/user_detail.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        access_list = UserBranchAccess.objects.filter(user_id=pk).values_list('branch_id')
        branch_list = Branch.objects.filter(id__in=access_list)
        context['branch_list'] = branch_list

        access_list = UserGroupAccess.objects.filter(user_id=pk).values_list('group_id')
        group_list = Group.objects.filter(id__in=access_list)
        context['group_list'] = group_list
        return context