from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Branch

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView 

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

    # def form_valid(self, request, *args, **kwargs):
    #     # logged_in_user = request.user
    #     # print(f'==========> {logged_in_user.email}')
    #     obj = self.get_object()
    #     return super(DeleteBranchView, self).delete(request, *args, **kwargs)
