from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm, UserPasswordChangeForm
from ..wishlist.models import Wishlist


def login_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        if request.POST.get('action') == 'login':
            login_form = LoginForm(data=request.POST)

            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']

                # Используем authenticate с параметром username (не email!)
                user = authenticate(request, username=email, password=password)

                if user:
                    # Используем стандартный login
                    login(request, user)
                    print(f"User logged in: {user.email}")
                    print(f"Session key: {request.session.session_key}")
                    return redirect('core:home')
                else:
                    print("Authentication failed")

        elif request.POST.get('action') == 'register':
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
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user # указатель на обновление существующей записи в форме
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:profile")

    else:
        form = ProfileForm(instance=request.user)

    context = {
        "orders_count": 0,
        "wishlist_count": wishlist_count,
        "form": form,
    }

    return render(request, "profile.html", context)


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "password_change_form.html"


def logout_view(request):
    logout(request)
    return redirect("core:home")
