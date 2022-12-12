from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from luvio_api.models import UserAccount
from luvio_api.serializers.user_account_serializer import UserAccountSerializer


class UserAccountView(APIView):

    def post(self, request):
        """Create new user account

        Args:
            request (_type_): _description_
        """
        # get username password from request
        # call serializer.save()
        # generate a token and return

    def get(self, request, format=None):
        """Get all existing accounts - for testing only, needs authentication

        Args:
            request (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)
