import datetime

from django.conf import settings
import jwt
from rest_framework import authentication, exceptions

from .models import CustomUser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return

        if len(auth_header) == 1:
            return

        elif len(auth_header) > 2:
            return

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception:
            msg = 'Токен испорчен'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = CustomUser.objects.get(pk=payload['id'])
        except CustomUser.DoesNotExist:
            msg = 'Пользователь соответствующий данному токену не найден.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token