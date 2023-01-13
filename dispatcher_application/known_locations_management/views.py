from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import LocationForm
from .models import Location
from django.contrib.postgres.search import SearchVector


# decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decorators import admin_permission
decorators = [login_required(), admin_permission()]


@method_decorator(decorators, name="dispatch")
class ListLocatiosView(ListView):
    model = Location
    template_name = 'known_locations_management/location_list.html'
    paginate_by = 25


    def get_queryset(self): 
        search_value = self.request.GET.get('search-box')
        self.filtered_by = ''
        self.search_val = ''
        if search_value is None or search_value.strip() == '':
           return Location.objects.all()

        self.search_val = search_value
        self.filtered_by = f'&search-box={search_value}'
        result = Location.objects.annotate(
            search=SearchVector('zip_code', 'city', 'country'),
            ).filter(search=search_value)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
        return context
        

@method_decorator(decorators, name="dispatch")
class AddLocationView(CreateView):
    model = Location
    template_name = 'known_locations_management/location_manage.html'
    success_url = reverse_lazy('location-list')
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Location'
        context['form_action_type'] = 'Add'
        return context


@method_decorator(decorators, name="dispatch")
class UpdateLocationView(UpdateView):
    model = Location
    template_name = 'known_locations_management/location_manage.html'
    success_url = reverse_lazy('location-list')
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Location'
        context['form_action_type'] = 'Update'
        return context


@method_decorator(decorators, name="dispatch")
class DeleteLocationView(DeleteView):
    model = Location
    template_name = 'known_locations_management/location_delete.html'
    success_url = reverse_lazy('location-list')

