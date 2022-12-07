from django.urls import path
from .views import UserCreationForm

urlpatterns = [
    path('create-user/', UserCreationForm.as_view(), name='user-creation'),
]