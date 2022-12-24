import bcrypt
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from luvio_api.models import UserAccount
from luvio_api.serializers import UserAccountSerializer


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        payload = request.data
        password = payload.get('password', None)
        username = self._get_username(payload)
        user = authenticate(request,
                            username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
            })
        else:
            raise exceptions.NotFound(
                "User not found - unable to authenticate!")

    def _get_username(self, payload: dict) -> str:
        if payload.get('email', None):
            return UserAccount.objects.get(email=payload['email']).username
        return payload.get('username', None)
