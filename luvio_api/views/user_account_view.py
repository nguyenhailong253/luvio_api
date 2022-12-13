from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from luvio_api.models import UserAccount
from luvio_api.serializers.user_account_serializer import RegistrationSerializer


class UserAccountView(APIView):

    def post(self, request: Request):
        """Create new user account

        Args:
            request (_type_): _description_
        """
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "success"})

    def get(self, request: Request):
        """Get all existing accounts - for testing only, needs authentication

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)
