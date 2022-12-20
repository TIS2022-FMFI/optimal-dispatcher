from django.urls import path
from transport_management.views import TransportationView#, EditTransportationView

urlpatterns = [
    # path('list/', ListTransportationsView.as_view(), name='transportation-list'),
    path('add/', TransportationView.as_view(), name='transportation-add'),
    #path('update/<int:pk>', EditTransportationView.as_view(), name='edit_transportation'),

]