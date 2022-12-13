from django.shortcuts import render
from django.views.generic.list import ListView
from transport_management.models import Transpotrations

class ListTransactionView(ListView):
    model = Transpotrations
    template_name = 'transport_viewer/transport_list.html'
    paginated_by = 25


