from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="groups"),
    path('add_group/', views.createGroup, name="add_group"),
    path('edit_group/<str:pk>/', views.updateGroup, name="update_group"),
    path('delete_group/', views.deleteGroup, name="delete_group"),
]
