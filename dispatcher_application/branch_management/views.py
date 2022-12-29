from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from django.http import HttpResponseRedirect, Http404

from django.contrib.postgres.search import SearchVector

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView 


from .forms import AddBranchAccessForm, AddBranch

############################
from access_management.models import UserBranchAccess 
from user_management.models import MyUser
from .models import Branch
###########################

class  BranchListView(ListView):
    model = Branch
    template_name = 'branch_management/branch_list.html'
    paginate_by = 25
    
    def get_queryset(self): 
        search_value = self.request.GET.get('search-box')
        self.filtered_by = ''
        self.search_val = ''
        if search_value is None or search_value.strip() == '':
           return Branch.objects.all()

        self.search_val = search_value
        self.filtered_by = f'&search-box={search_value}'
        result = Branch.objects.annotate(
            search=SearchVector('name'),
            ).filter(search=search_value)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
        return context


class AddBranchView(CreateView):
    model = Branch
    template_name = 'branch_management/branch_add.html'
    success_url = reverse_lazy('branch-list')
    form_class = AddBranch
    


class UpdateBranchView(UpdateView):
    model = Branch
    template_name = 'branch_management/branch_update.html'
    success_url = reverse_lazy('branch-list')
    form_class = AddBranch


class DeleteBranchView(DeleteView):
    model = Branch
    template_name = 'branch_management/branch_delete.html'
    success_url = reverse_lazy('branch-list')


    def form_valid(self, form):
        success_url = self.get_success_url()
        user = self.request.user
        pk = self.kwargs['pk']
        if user.branch_id != pk:
            self.object.delete()
        return HttpResponseRedirect(success_url)


class BranchAccessView(DetailView):
    model = Branch
    template_name = 'branch_management/branch_access.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        access_list = UserBranchAccess.objects.filter(branch_id=pk).values_list('user_id')
        users_with_access = MyUser.objects.filter(Q(id__in=access_list) | Q(branch_id=pk))
        context['users'] = users_with_access
        return context


class AddAccessView(CreateView):
    template_name = 'branch_management/branch_access_add.html'
    form_class = AddBranchAccessForm
    success_url = reverse_lazy('branch-list')


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        kwargs = self.get_form_kwargs()
        kwargs['branch_id'] = self.kwargs['pk']
        return form_class(**kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['branch_id'] = pk
        return context
   


class RemoveAccessView(DeleteView):
    model = UserBranchAccess
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

        queryset = UserBranchAccess.objects.filter(branch_id=branch, user_id=user)

        if not queryset:
           raise Http404

        return queryset



    