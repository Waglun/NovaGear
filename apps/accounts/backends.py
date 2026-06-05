from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):

        print("BACKEND CALLED")
        print("email arg =", email)
        print("username arg =", username)
        print("kwargs =", kwargs)

        email = email

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None