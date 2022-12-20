from django.urls import path
from transport_management.views import TransportationView, EditTransportationView

urlpatterns = [
    path('add', TransportationView.as_view(), name='add_transportation'),
    path('edit/<int:pk>', EditTransportationView.as_view(), name='edit_transportation'),

]