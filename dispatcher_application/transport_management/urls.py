from django.urls import path
from transport_management.views import ListTransportationsView, AddTransportationView, UpdateTransportationView

urlpatterns = [
    path('list/', ListTransportationsView.as_view(), name='transportation-list'),
    path('add/', AddTransportationView.as_view(), name='transportation-add'),
    path('update/<int:pk>', UpdateTransportationView.as_view(), name='transportation-update'),
]
