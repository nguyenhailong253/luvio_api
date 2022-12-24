from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import UserAccount
from luvio_api.serializers import UserAccountSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        """
        Register a new user account and return auth token
        """
        serializer = UserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )
