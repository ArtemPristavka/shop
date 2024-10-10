from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from typing import Any



class UserRegisterView(CreateView):
    "View for register user"
    
    form_class = UserCreationForm
    template_name = "my_auth/register.html"
    success_url = reverse_lazy("shop:products-list")
    
    def get(
        self,
        request: HttpRequest, 
        *args: str, 
        **kwargs: reverse_lazy) -> HttpResponse: # type: ignore
        """
        Call method Get where: 
            if user is authenticated to redirect on product-list
            else returning form register
        """
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Creating new user and login now

        Args:
            form (UserCreationForm): _description_

        Returns:
            HttpResponseRedirect: redirect on 'accounts/about-me/<int:pk>/' 
                                                -> my_auth:about-me
        """
        
        self.object = form.save()
        
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(self.request, user)
        
        return HttpResponseRedirect(self.get_success_url())
    
    # def get_success_url(self) -> str:
    #     "Redirect new autheticeted user on page user"
        
    #     return reverse("my_auth:about-user", kwargs={"pk": self.request.user.pk})
    

class UserLoginView(LoginView):
    "View for completing authenticating (login) on site"
    
    redirect_authenticated_user = True
    next_page = reverse_lazy("shop:products-list")
    template_name = "my_auth/login.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    "View for completing logout from site"
    
    next_page = reverse_lazy("shop:products-list")


class UserInfoView(LoginRequiredMixin, TemplateView):
    "View for show info about user"
    
    template_name = "my_auth/about-me.html"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        # print(f"page last: {self.request.META.get('HTTP_REFERER')}")
        # print(f"page last -> split: {self.request.META.get('HTTP_REFERER').split('/', 3)[3]}")
        
        kwargs["object"] = User.objects.get(pk=self.request.user.pk)
        return super().get_context_data(**kwargs)
    