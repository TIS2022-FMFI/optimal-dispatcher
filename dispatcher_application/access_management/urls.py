from django.urls import path
from .views import ListGroupsView, CreateGroupView, UpdateGroupView, DeleteGroupView, GroupAccessView, AddGroupAccessView, DeleteGroupAccessView, NotFoundView


urlpatterns = [
    path('group/list/', ListGroupsView.as_view(), name="group-list"),
    path('group/add/', CreateGroupView.as_view(), name="group-add"),
    path('group/update/<int:pk>/', UpdateGroupView.as_view(), name="group-update"),
    path('group/delete/<int:pk>/', DeleteGroupView.as_view(), name="group-delete"),

    # group access management view
    path('group/access/<int:pk>/', GroupAccessView.as_view(), name="group-access"),
    path('group/access/<int:pk>/add/', AddGroupAccessView.as_view(), name="group-access-add"),
    path('group/access/<int:pk>/delete/<int:upk>', DeleteGroupAccessView.as_view(), name="group-access-delete"),
    
    # redirect to 404 template
    path('page-not-found', NotFoundView.as_view(), name='page-not-found'),
]

