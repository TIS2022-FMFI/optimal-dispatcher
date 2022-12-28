from django.shortcuts import render
from django.urls import reverse_lazy

# view imports
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormView

# model imports
from .models import MyUser

from django.contrib.postgres.search import SearchVector

from .user_form import CreateRegistrationForm, CustomUserChangeForm


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
            search=SearchVector('last_name'),
            ).filter(search=search_value)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
        return context
    

class RegisterNewUserView(CreateView):
    model = MyUser
    template_name = 'user_management/user_add.html'
    form_class = CreateRegistrationForm
    # fields = ['first_name', 'last_name', 'email', 'password', 'branch', 'is_superuser']
    success_url = reverse_lazy('user-list')


class UpdateUserView(UpdateView):
    model = MyUser
    template_name = 'user_management/user_update.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user-list')


class DeleteUserView(DeleteView):
    model = MyUser
    template_name = 'user_management/user_delete.html'
    success_url = reverse_lazy('user-list')

