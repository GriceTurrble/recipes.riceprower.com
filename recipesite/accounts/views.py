from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. Come back soon!")
    return redirect("/")
