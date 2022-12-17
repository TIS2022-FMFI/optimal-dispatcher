from django.shortcuts import render
from django.views.generic.list import ListView
from transport_management.models import Transportations

class ListTransactionView(ListView):
    model = Transportations
    template_name = 'transport_viewer/transport_list.html'
    paginated_by = 25


