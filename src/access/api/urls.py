from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.api_login, name="api_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path(
        "check-username/<str:username>/",
        views.check_username,
        name="check-username",
    ),
    path("change-password/", views.change_password, name="change-password"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.profile_update, name="profile-update"),
]
