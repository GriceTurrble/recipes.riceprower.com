# from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ("email", "username", "password1", "password2")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email / Username")
