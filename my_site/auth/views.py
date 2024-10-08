from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView



class UserRegisterView(CreateView):
    "View for register user"
    
    template_name = ""
    success_url = reverse_lazy("")


class UserLoginView(LoginView):
    pass


class UserLogoutView(LogoutView):
    pass


class UserInfoView(DetailView):
    "View for show info about user"
    
    template_name = ""
