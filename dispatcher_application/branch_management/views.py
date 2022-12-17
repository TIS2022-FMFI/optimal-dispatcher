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
    # template = 'branch_management/branch_access_add.html'
    # model = User_branch_access
    template_name = 'branch_management/branch_access_add.html'
    form_class = AddBranchAccessForm
    success_url = reverse_lazy('branch-list')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        kwargs = self.get_form_kwargs()

        pk = self.kwargs['pk']
        kwargs['branch_id'] = pk

        return form_class(**kwargs)
    # fields = [ 'user_id', 'branch_id']

    # def get(self, request):
    #     context = {}
    #     return render(request, "access_management/group_main.html", context)

    # def post(self, request):
    #     ...


# class RemoveAccessView(DeleteView):
#     model = User_branch_access
#     template_name = 'branch_management/branch_access_remove.html'
#     success_url = reverse_lazy('branch-list')


    # model = ReportSchedule
    # template_name = "report/report_confirm_delete.html"
    # success_url = lazy(reverse, str)('jsclient-list')

    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()

    #     branch = self.kwargs['pk']
    #     user = self.kwargs['upk']

    #     queryset = User_branch_access.objects.filter(branch_id=branch, user_id=user)

    #     if not queryset:
    #        raise Http404

    #     context = { 'branch_id':branch, 'user_id':user }
    #     print('------------------------------------------')
    #     return context

    # # Override the delete function to delete report Y from client X
    # # Finally redirect back to the client X page with the list of reports
    # def delete(self, request, *args, **kwargs):
    #     branch = self.kwargs['pk']
    #     user = self.kwargs['upk']
        
    #     remove_access = User_branch_access.objects.filter(branch_id=branch, user_id=user)
        
    #     print(remove_access)
    #     remove_access.delete()


# class RemoveAccessView(View):
#     # model = User_branch_access
#     # template_name = 'branch_management/branch_access_remove.html'
#     # success_url = reverse_lazy('branch-list')

#     template = 'branch_management/branch_access_remove.html'

#     def get(self, request):
#         to_remove_access = request.GET.getlist("remove_data")

#         users = []
#         for selected_id in to_remove_access:
#             users.append(MyUser.objects.get(id=selected_id))
          
#         context = { 'users' : users }
#         return render(request, self.template, context)


#     def post(self, request):
#         # User_branch_access.objects.filter(branch_id=pk).values_list('user_id')

#         x = request.POST.getlist("remove_data")
#         print('---------------------------0')
#         print(x)
#         return redirect('branch-list') #redirect('branch-access', pk=3)
 
    #     pole = request.POST.getlist("data")
    #     print(pole)
    #     for i in pole:
    #         obj = User_branch_access.objects.get(id=i)
    #         obj.delete()

    #     return redirect(request.META.get('HTTP_REFERER', 'list-of-branches/'))

    #     groups = Groups.objects.all()
    #     context = {"groups":groups}
    #     return render(request, "access_management/group_main.html", context)