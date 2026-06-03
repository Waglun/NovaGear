from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterForm, LoginForm


def login_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect(f"{reverse('accounts:login')}#login")
        else:
            print(register_form.errors)

    return render(
        request,
        'login.html',
        {
            "login_form": login_form,
            "register_form": register_form,
        },
    )


@login_required
def profile_view(request):
    return render(request, "profile.html")


def logout_view(request):
    logout(request)
    return redirect("core:home")
