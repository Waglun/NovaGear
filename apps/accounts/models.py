from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    Username = models.CharField(
        max_length=20,
        blank=True
    )
    email =models.EmailField(
        max_length=20,
        blank=True
    )
    Password = models.CharField(max_length=20)
    Conf_password = models.CharField(max_length=20)