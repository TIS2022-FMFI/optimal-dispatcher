from django.shortcuts import render
from django.urls import reverse_lazy

# view imports
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormView

# model imports
from .models import MyUser


from .user_form import CreateRegistrationForm, CustomUserChangeForm


class ListAllUsersView(ListView):
    model = MyUser
    template_name = 'user_management/user_list.html'
    paginate_by = 25
    


class RegisterNewUserView(CreateView):
    model = MyUser
    template_name = 'user_management/user_add.html'
    form_class = CreateRegistrationForm
    # fields = ['first_name', 'last_name', 'email', 'password', 'branch', 'is_superuser']
    success_url = reverse_lazy('user-list')


class UpdateUserView(UpdateView):
    model = MyUser
    template_name = 'user_management/user_update.html'
    fields = ['first_name', 'last_name', 'branch', 'is_superuser']
    # form_class = CustomUserChangeForm
    success_url = reverse_lazy('user-list')


class DeleteUserView(DeleteView):
    model = MyUser
    template_name = 'user_management/user_delete.html'
    success_url = reverse_lazy('user-list')

