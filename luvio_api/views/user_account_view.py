from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import UserAccount
from luvio_api.serializers import UserAccountSerializer


class UserAccountView(APIView):
    def get(self):
        """
        Get all existing accounts - for testing only
        """
        accounts = get_list_or_404(UserAccount)
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def put(self, request: Request):
        """
        Update an existing account's details (excluding password)
        """
        current_account = request.user
        account = get_object_or_404(UserAccount, pk=current_account.id)
        account.email = request.data.get("email", account.email)
        account.username = request.data.get("username", account.username)
        account.first_name = request.data.get("first_name", account.first_name)
        account.last_name = request.data.get("last_name", account.last_name)
        account.date_of_birth = request.data.get("date_of_birth", account.date_of_birth)
        account.mobile = request.data.get("mobile", account.mobile)
        try:
            account.save()
        except Exception as e:
            raise exceptions.ValidationError(
                {"message": f"Unable to update account - {e}"}
            )
        return Response({"message": "Successfully updated account!"})
