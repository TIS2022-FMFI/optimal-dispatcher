from django.urls import path
from .views import ListAllUsersView, RegisterNewUserView, UpdateUserView, DeleteUserView

urlpatterns = [
    path('list-of-users/', ListAllUsersView.as_view(), name='user-list'),
    path('add-user/', RegisterNewUserView.as_view(), name='user-add'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='user-update'),
    path('delete-user/<int:pk>', DeleteUserView.as_view(), name='user-delete')
]