from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

UserModel = get_user_model()


class MyBackend(BaseBackend):
    def authenticate(self, request, email=None, confcode=None):
        if email is None or confcode is None:
            return
        else:
            return user
        '''    
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return
        return user

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user
