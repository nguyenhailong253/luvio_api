from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from luvio_api.models import UserAccount
from luvio_api.serializers.user_account_serializer import UserAccountSerializer


class UserAccountViews(APIView):

    def get(self, request, format=None):
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)
