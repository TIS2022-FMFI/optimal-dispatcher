from django.shortcuts import render
from django.urls import reverse_lazy

# view imports
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import MyUser
from .forms import CustomUserCreateForm, CustomUserUpdateForm


class ListAllUsersView(ListView):
    model = MyUser
    template_name = 'user_management/user_list.html'
    paginate_by = 25
    

class RegisterNewUserView(CreateView):
    model = MyUser
    template_name = 'user_management/user_add.html'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('user-list')


class UpdateUserView(UpdateView):
    model = MyUser
    template_name = 'user_management/user_update.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('user-list')


class DeleteUserView(DeleteView):
    model = MyUser
    template_name = 'user_management/user_delete.html'
    success_url = reverse_lazy('user-list')

