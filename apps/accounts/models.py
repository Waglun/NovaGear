from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )

    avatar = models.ImageField(
        "Аватар", # Позиционный параметр verbose_name
        upload_to="accounts/avatars",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        verbose_name="Телефон",
        max_length=20,
        blank=True,
    )

    birthday = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        "Дата регистрации",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата изменения",
        auto_now=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


# class Address(models.Model):
#     user = models.ForeignKey(User,)