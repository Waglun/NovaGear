from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .session import SessionCart


@receiver(user_logged_in)
def merge_session_cart(sender, request, user, **kwargs):
    SessionCart(request).merge_to_database(user)