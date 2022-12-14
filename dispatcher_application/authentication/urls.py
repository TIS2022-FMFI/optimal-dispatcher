from django.urls import path
from .views import LoginView#, CustomLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    

    # reset password via email
    # path('password-reset/', auth_views.PasswordResetView.as_view(
    #     template_name="authentication/reset_password.html"), name="password_reset"),

    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name="authentication/reset_password_confirm.html"), name="password_reset_confirm"),

    # path('sent-password-reset/', auth_views.PasswordResetDoneView.as_view(
    #     template_name="authentication/reset_password_done.html"), name="password_reset_done"),
        
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name="authentication/reset_password_complete.html"), name="password_reset_complete"),
]
