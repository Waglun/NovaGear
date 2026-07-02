from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Min. 6 characters"}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"}))

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "ProGamer_42",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "input",
                "name": "email",
                "placeholder": "you@email.com",
                "autocomplete": "email",
            })
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "email",
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "input"
            }
        )
    )