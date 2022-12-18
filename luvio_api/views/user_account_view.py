from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from luvio_api.models import UserAccount
from luvio_api.serializers.user_account_serializer import RegistrationSerializer, UserAccountSerializer


class UserAccountView(APIView):
    # Setting a class attribute to override the default permissions_classes with something that will use our Access Token properly.
    # Ref: https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_03.html
    permission_classes = [TokenHasReadWriteScope]

    def post(self, request: Request):
        """
        Create new user account
        """
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "success"})

    def get(self, request: Request):
        """
        Get all existing accounts - for testing only
        """
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)
