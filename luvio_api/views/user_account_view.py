from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import UserAccount


class UserAccountView(APIView):
    def put(self, request: Request) -> Response:
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


# Ref: https://stackoverflow.com/a/33389526/8749888
@api_view(["PUT"])
def change_password(request: Request) -> Response:
    current_account = request.user
    if current_account.check_password(request.data.get("old_password", None)):
        new_password = request.data.get("new_password", None)
        if new_password:
            current_account.set_password(new_password)
            current_account.save()
            return Response(
                {"message": "Successfully changed password!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        raise exceptions.ValidationError({"message": "New password cannot be empty"})
    raise exceptions.ValidationError({"message": "Incorrect old password"})
