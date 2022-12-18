from django.urls import path
from .views import BranchListView, AddBranchView, UpdateBranchView, DeleteBranchView, BranchAccessView, AddAccessView, RemoveAccessView


urlpatterns = [
    # branch management
    path('list/', BranchListView.as_view(), name='branch-list'),
    path('add/', AddBranchView.as_view(), name='branch-add'),
    path('update/<int:pk>/', UpdateBranchView.as_view(), name='branch-update'),
    path('delete/<int:pk>/', DeleteBranchView.as_view(), name='branch-delete'),

    # branch access management
    path('access/<int:pk>/', BranchAccessView.as_view(), name='branch-access'),
    path('access/<int:pk>/add/', AddAccessView.as_view(), name='branch-access-add'),
    path('access/<int:pk>/delete/<int:upk>', RemoveAccessView.as_view(), name='branch-access-delete'),
]
