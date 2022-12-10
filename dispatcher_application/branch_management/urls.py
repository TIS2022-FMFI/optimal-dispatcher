from django.urls import path
from .views import BranchListView, AddBranchView, UpdateBranchView, DeleteBranchView


urlpatterns = [
    path('list-of-branches/', BranchListView.as_view(), name='branch-list'),
    path('add-branch/', AddBranchView.as_view(), name='branch-add'),
    path('update-branch/<int:pk>', UpdateBranchView.as_view(), name='branch-update'),
    path('delete-branch/<int:pk>', DeleteBranchView.as_view(), name='branch-delete'),
]
