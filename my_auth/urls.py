from django.urls import re_path

from my_auth.views import (
    LoginView,
    LogoutView,
    UserDetailView,
    UserListView,
    UserRegisterView,
)

# example of generic endpoints

users_urls = [
    re_path(
        r"^users/?$",
        UserListView.as_view(),
        name="users",
    ),
    re_path(
        r"^users/(?P<pk>[0-9]+)/?$",
        UserDetailView.as_view(),
        name="user",
    ),
    re_path(r"^login/", LoginView.as_view(), name="login"),
    re_path(r"^logout/", LogoutView.as_view(), name="logout"),
    re_path(r"^register/", UserRegisterView.as_view(), name="register"),
]

urlpatterns = users_urls
