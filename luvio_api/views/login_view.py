import bcrypt

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate

from luvio_api.serializers import UserAccountSerializer
from luvio_api.models import UserAccount


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        password = payload.get('password', None)
        username = self.get_username(payload)
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

    def get_username(self, payload: dict) -> str:
        if payload.get('email', None):
            return UserAccount.objects.get(email=payload['email']).username
        return payload.get('username', None)
