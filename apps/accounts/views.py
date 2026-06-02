from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, "register.html")

@login_required
def profile_view(request):
    return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("core:home")
