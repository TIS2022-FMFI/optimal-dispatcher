from django.urls import path
from .views import ListLocatiosView, AddLocationView, UpdateLocationView, DeleteLocationView

urlpatterns = [
    path('list/', ListLocatiosView.as_view(), name='location-list'),
    path('add/', AddLocationView.as_view(), name='location-add'),
    path('update/<int:pk>', UpdateLocationView.as_view(), name='location-update'),
    path('delete/<int:pk>', DeleteLocationView.as_view(), name='location-delete'),
]