from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


from .forms import RegisterForm, LoginForm


def login_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        if request.POST.get('action') == 'login':
            login_form = LoginForm(data=request.POST)

            print("LOGIN FORM SUBMITTED")
            if login_form.is_valid():
                print("FORM IS VALID")
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']

                user = authenticate(request, email=email, password=password)

                if user:
                    login(request, user)
                    return redirect('core:home')
                print(user)

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
    return render(request, "profile.html")


def logout_view(request):
    logout(request)
    return redirect("core:home")
