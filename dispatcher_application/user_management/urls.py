from django.urls import path
from .views import ListAllUsersView, RegisterNewUserView, UpdateUserView, DeleteUserView, UserDetailView

urlpatterns = [
    path('list/', ListAllUsersView.as_view(), name='user-list'),
    path('add/', RegisterNewUserView.as_view(), name='user-add'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='user-update'),
    path('delete/<int:pk>', DeleteUserView.as_view(), name='user-delete'),
    path('detail/<int:pk>', UserDetailView.as_view(), name='user-detail')
]