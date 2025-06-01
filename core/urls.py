from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import register, profile, edit_profile, user_profile, landing_page,logout_view

app_name = 'core'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),

    # profile related
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
   path("profile/<str:username>/", user_profile, name="user_profile"),

    # password reset
    path("password_reset/", PasswordResetView.as_view(template_name="core/password_reset.html"), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),
    path("", landing_page, name="home")
]
