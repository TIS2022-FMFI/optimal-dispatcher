from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="transport_data"),
    path('add_transport/', views.createTransport, name="add_transport"),
    path('edit_transport/<str:pk>/', views.updateTransport, name="update_transport"),
    path('delete_transport/', views.deleteTransport, name="delete_transport"),
]
