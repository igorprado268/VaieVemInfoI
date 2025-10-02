from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Backend de autenticação que permite login com email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Tenta encontrar usuário pelo email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        # Verifica a senha
        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
