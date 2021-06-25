from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.tokens import default_token_generator as token

UserModel = get_user_model()


class MyBackend(BaseBackend):
    def authenticate(self, email=None, confcode=None):
        if email is None or confcode is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return
        else:
            if token.check_token(user, confcode):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user
