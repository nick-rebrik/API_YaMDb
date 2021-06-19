from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password,check_password
from api.models import ConfCode

UserModel = get_user_model()

class MyBackend(BaseBackend):
    def authenticate(self, request, email=None, confcode=None):
        if email is None or confcode is None:
            return 
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return 
        else:
            try:
                check = ConfCode.objects.get(email=email)
            except ConfCode.DoesNotExist:
                return 
            else:
                # проверяем, совпадает ли зашифрованный код в базе
                # c кодом из запроса
                if check_password(confcode, check.confcode):
                    return user
    
    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user 
            
        

        