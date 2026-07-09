from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views
from .forms import PasswordResetConfirmCustomForm, PasswordResetCustomForm
from .views import UserPasswordChange

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),

    path("password_change/", UserPasswordChange.as_view(), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),


    path('password_reset/', PasswordResetView.as_view(              # страница ввода email для смены пароля
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            form_class=PasswordResetCustomForm,
            success_url=reverse_lazy('accounts:password_reset_done'),
    ), name='password_reset'),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'), # страница с информацией о смене пароля

    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            form_class=PasswordResetConfirmCustomForm,
            success_url=reverse_lazy('accounts:password_reset_complete'),
         ), name='password_reset_confirm'), # одноразовая ссылка из письма для смены пароля

    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'), #  информация что пароль успешно изменен
]