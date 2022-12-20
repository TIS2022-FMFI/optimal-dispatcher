from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.db import transaction

from django.views.generic.list import ListView
from django.views.generic import CreateView, DeleteView, FormView

from .forms import GroupAddForm, GroupUpdateForm

from .models import Group, GroupBranchAccess
from branch_management.models import Branch

from django.db import IntegrityError
from django.db.models import Q


class ListGroupsView(ListView):
    model = Group
    template_name = 'access_management/group_list.html'
    paginate_by = 20


class CreateGroupView(FormView):
    template_name = 'access_management/group_add.html'
    form_class = GroupAddForm
    success_url = reverse_lazy('group-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Create Group'
        context['form_action_type'] = 'Add'
        return context


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



class UpdateGroupView(FormView):
    template_name = 'access_management/group_add.html'
    form_class = GroupUpdateForm
    success_url = reverse_lazy('group-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Group'
        context['form_action_type'] = 'Update'
        return context


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        kwargs = self.get_form_kwargs()
        kwargs['g_id'] = self.kwargs['pk']
        return form_class(**kwargs)


    def form_valid(self, form):
        form_fields = form.cleaned_data
        pk = self.kwargs['pk']

        group = Group.objects.get(id=pk)
        group_access_list = {obj.branch_id for obj in GroupBranchAccess.objects.filter(group_id=pk)}
        new_group_access_list = {Branch.objects.get(id=b_id) for b_id in form_fields['branch']}

        to_delete_access = group_access_list - new_group_access_list
        to_add_access = new_group_access_list - group_access_list 
        
        try:
            with transaction.atomic():
                # to_delete_branch_id_list = [obj.id for obj in to_delete_access]
                to_delete_access_list = GroupBranchAccess.objects.filter(Q(group_id=group) & Q(branch_id__in=to_delete_access))
                for obj in to_delete_access_list:
                    obj.delete()

                for branch in to_add_access:
                    GroupBranchAccess.objects.create(group_id=group, branch_id=branch)
        except IntegrityError:
            ...
        return HttpResponseRedirect(self.get_success_url())


class DeleteGroupView(DeleteView):
    model = Group
    template_name = 'access_management/group_delete.html'
    success_url = reverse_lazy('group-list')













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

