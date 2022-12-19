from django.urls import path
from .views import ListGroupsView, CreateGroupView, UpdateGroupView, DeleteGroupView


urlpatterns = [
    path('group/list/', ListGroupsView.as_view(), name="group-list"),
    path('group/add/', CreateGroupView.as_view(), name="group-add"),
    # path('group/update/<int:pk>/', UpdateGroupView.as_view(), name="group-update"),
    path('group/delete/<int:pk>/', DeleteGroupView.as_view(), name="group-delete"),

    # # group access management view
    # path('group/add/<int:pk>/', GroupAccessView.as_view(), name="group-access"),
    # path('group/add/<int:pk>/add/', AddGroupAccessView.as_view(), name="group-access-add"),
    # path('group/add/<int:pk>/delete/<int:upk>', DeleteGroupAccessView.as_view(), name="group-access-delete"),


    # path('', views.main, name="groups"),
    # path('group/update/<str:pk>/', views.updateGroup, name="update_group"),
    # path('group/delete/', views.deleteGroup, name="delete_group"),
]

