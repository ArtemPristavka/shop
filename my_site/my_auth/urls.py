from django.urls import path

from .views import (
    UserInfoView, UserRegisterView, UserLogoutView, UserLoginView
    )


app_name = "my_auth"

urlpatterns = [
    path("about-me/<int:pk>/", UserInfoView.as_view(), name="about-user"),
    path("register/", UserRegisterView.as_view(), name="register-user"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("login/", UserLoginView.as_view(), name="login")
]