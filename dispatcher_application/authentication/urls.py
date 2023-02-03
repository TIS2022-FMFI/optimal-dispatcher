from django.urls import path
from .views import CustomLoginView, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout'),
    

    # reset password via email
    path('password-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('sent-password-reset/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
