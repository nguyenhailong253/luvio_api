import logging

from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import UserAccount

logger = logging.getLogger(DEFAULT_LOGGER)


class LoginView(ObtainAuthToken):
    """
    Handling user logging in and token generation
    """

    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Accept both email or username (eventually convert both to username) and password
        for authentication
        """
        payload = request.data
        password = payload.get("password", None)
        username = self._get_username(payload)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user_id": user.pk,
                    "email": user.email,
                    "username": user.username,
                }
            )
        logger.error(f"Unable to log in - Incorrect username '{username}' or password")
        raise exceptions.NotFound("Incorrect username or password - unable to log in!")

    def _get_username(self, payload: dict) -> str:
        if payload.get("email", None):
            return UserAccount.objects.get(email=payload["email"]).username
        return payload.get("username", None)
