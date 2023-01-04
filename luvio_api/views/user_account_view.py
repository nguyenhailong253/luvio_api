import logging

from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import UserAccount
from luvio_api.serializers import UserAccountSerializer

logger = logging.getLogger(DEFAULT_LOGGER)


class UserAccountView(APIView):
    """
    Technically a DETAIL view - only handle update at the moment
    """

    def put(self, request: Request) -> Response:
        """
        Update an existing account's details (excluding password)
        """
        account = get_object_or_404(UserAccount, pk=request.user.id)
        serializer = UserAccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            logger.exception(f"Update account failed - {e}")
            raise exceptions.ValidationError(
                {"message": f"Unable to update account - {e}"}
            )
        return Response({"message": "Successfully updated account!"})


# Ref: https://stackoverflow.com/a/33389526/8749888
@api_view(["PUT"])
def change_password(request: Request) -> Response:
    """
    Handle password change request. Need to provide both old password and new password
    """
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
