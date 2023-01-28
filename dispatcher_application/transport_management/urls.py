from django.urls import path
from transport_management.views import ListTransportationsView, TransportationAddView, TransportationUpdateView, TransportationDetailView, TransportationDeleteView

urlpatterns = [
    path('list/', ListTransportationsView.as_view(), name='transportation-list'),
    path('add/', TransportationAddView.as_view(), name='transportation-add'),
    path('update/<int:pk>', TransportationUpdateView.as_view(), name='transportation-update'),
    path('detail/<int:pk>', TransportationDetailView.as_view(), name='transportation-detail'),
    path('delete/', TransportationDeleteView.as_view(), name='transportation-delete'),
]