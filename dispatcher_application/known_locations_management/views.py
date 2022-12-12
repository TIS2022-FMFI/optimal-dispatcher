from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Location

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


class ListLocatiosView(ListView):
    model = Location
    template_name = 'known_locations_management/location_list.html'
    paginate_by = 25


class AddLocationView(CreateView):
    model = Location
    template_name = 'known_locations_management/location_add.html'
    success_url = reverse_lazy('location-list')
    fields = ['zip_code', 'city', 'country']


class UpdateLocationView(UpdateView):
    model = Location
    template_name = 'known_locations_management/location_update.html'
    success_url = reverse_lazy('location-list')
    fields = ['zip_code', 'city', 'country']


class DeleteLocatonView(DeleteView):
    model = Location
    template_name = 'known_locations_management/location_delete.html'
    success_url = reverse_lazy('location-list')

