from django.urls import path
from .views import ListLocatiosView, AddLocationView, UpdateLocationView, DeleteLocatonView

urlpatterns = [
    path('list-of-locations/', ListLocatiosView.as_view(), name='location-list'),
    path('add-location/', AddLocationView.as_view(), name='location-add'),
    path('update-location/<int:pk>', UpdateLocationView.as_view(), name='location-update'),
    path('delete-location/<int:pk>', DeleteLocatonView.as_view(), name='location-delete'),
]