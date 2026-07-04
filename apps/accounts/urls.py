from django.urls import path
from . import views
from .views import UserPasswordChange

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("password_change/", UserPasswordChange.as_view(), name="password_change"),
]