from django.urls import path
from .views import UserSettingsView, ChangePasswordView


urlpatterns = [
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('settings/password-change', ChangePasswordView.as_view(), name='user-password-change'),
]