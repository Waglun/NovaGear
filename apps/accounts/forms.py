from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from .utils import StyledFieldsMixin


class RegisterForm(StyledFieldsMixin, UserCreationForm):
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


class LoginForm(StyledFieldsMixin, forms.Form):
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


class ProfileForm(StyledFieldsMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].disabled = True # Запрет на изменение поля Email

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "phone",
            "birthday",
            "avatar",
        )
        # Подключение стилей
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Display name",
                "autocomplete": "username",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+7 (999) 123-45-67",
                "autocomplete": "tel",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }),
            "birthday": forms.DateInput(attrs={
                "type": "date",
            }),
            "avatar": forms.FileInput(attrs={
                "accept": "image/*",
            }),
        }

        labels = {
            "username": "Display name",
            "phone": "Phone",
            "email": "Email",
            "birthday": "Birth date",
            "avatar": "Avatar",
        }

        help_texts = {
            "username": "",
        }

        def clean_phone(self):
            phone = self.cleaned_data["phone"]
            if phone:
                phone = phone.strip()
            return phone

        error_css_class = "field-error"

        required_css_class = "required"


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                "class": "input"
            })


class PasswordResetConfirmCustomForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input",
            })


class PasswordResetCustomForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "input",
            "placeholder": "Enter your email",
        })