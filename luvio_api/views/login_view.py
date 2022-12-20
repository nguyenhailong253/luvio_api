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
        if payload.get('email', None):
            username = UserAccount.objects.get(email=payload['email']).username
        username = payload.get('username')
        user = authenticate(request,
                            username=username, password=password)
        if user is not None:
            print(f"user: {user}")
            token, created = Token.objects.get_or_create(user=user)
            print(f"token: {token}")
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
            })
        else:
            raise exceptions.NotAuthenticated(
                "User not found - unable to authenticate!")
