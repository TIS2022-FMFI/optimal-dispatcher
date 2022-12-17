from django.urls import path
from .views import ManageUserBranchesView, TestTempView



urlpatterns = [
    path('manage-user-branches/', ManageUserBranchesView.as_view(), name='user-branch-management'),
    path('test-temp/', TestTempView.as_view(), name='test-temp'),
]