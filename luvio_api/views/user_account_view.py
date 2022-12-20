from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from luvio_api.models import UserAccount
from luvio_api.serializers import UserAccountSerializer


class UserAccountView(APIView):

    def get(self, request: Request, format=None):
        """
        Get all existing accounts - for testing only
        """
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)
