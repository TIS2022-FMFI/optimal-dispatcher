from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.http import Http404

from .models import Branch

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from django.views.generic.list import ListView 


from .forms import AddBranchAccessForm

############################
from access_management.models import User_branch_access
from user_management.models import MyUser

###########################

class  BranchListView(ListView):
    model = Branch
    template_name = 'branch_management/branch_list.html'
    paginate_by = 20


class AddBranchView(CreateView):
    model = Branch
    template_name = 'branch_management/branch_add.html'
    success_url = reverse_lazy('branch-list')

    fields = [ 'name' ]


class UpdateBranchView(UpdateView):
    model = Branch
    template_name = 'branch_management/branch_update.html'
    success_url = reverse_lazy('branch-list')

    fields = [ 'name' ]


class DeleteBranchView(DeleteView):
    model = Branch
    template_name = 'branch_management/branch_delete.html'
    success_url = reverse_lazy('branch-list')


class BranchAccessView(DetailView):
    model = Branch
    template_name = 'branch_management/branch_access.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        access_list = User_branch_access.objects.filter(branch_id=pk).values_list('user_id')
        users_with_access = MyUser.objects.filter(id__in=access_list)
        context['users'] = users_with_access
        return context


class AddAccessView(CreateView):
    template_name = 'branch_management/branch_access_add.html'
    form_class = AddBranchAccessForm
    success_url = reverse_lazy('branch-list')


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        pk = self.kwargs['pk']

        kwargs = self.get_form_kwargs()
        kwargs['branch_id'] = pk
        return form_class(**kwargs)
   


class RemoveAccessView(DeleteView):
    model = User_branch_access
    template_name = 'branch_management/branch_access_delete.html'
    success_url = reverse_lazy('branch-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upk = self.kwargs['upk']
        user = MyUser.objects.get(id=upk)
        context['user'] = user
        return context


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        branch = self.kwargs['pk']
        user = self.kwargs['upk']

        queryset = User_branch_access.objects.filter(branch_id=branch, user_id=user)

        if not queryset:
           raise Http404

        return queryset
