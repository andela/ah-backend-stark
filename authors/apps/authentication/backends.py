import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """Configure JWT Here"""

    def authenticate(self, request):

        token = request.META.get('HTTP_TOKEN', None)

        if not token:
            return None

        return self.get_authentication_credencials(request, token)

    def get_authentication_credencials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        payload = self.decode_token(token)
        user = self.get_user(payload)

        if not user.is_verified:
            msg = (
                "This user account is not verified. " +
                "Check your email for activation link")
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

    def get_verification_credencials(self, request, token):
        """
            Try to authenticate the given credentials. If authentication is
            successful, return the user and token. If not, throw an error.
            """

        payload = self.decode_token(token)
        user = self.get_user(payload)

        return (user, token)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            msg = 'The token is invalid'
            raise exceptions.AuthenticationFailed(msg)

        return payload

    def get_user(self, payload):
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'This token does not belong to any user'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user
