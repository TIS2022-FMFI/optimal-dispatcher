from django.urls import path
from transport_management.views import TransportationView

urlpatterns = [
    path('add', TransportationView.as_view(), name='add_transportation'),
]