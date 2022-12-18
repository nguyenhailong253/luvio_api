from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from luvio_api.models import ProfileType
from luvio_api.serializers.profile_type_serializer import ProfileTypeSerializer


class ProfileTypeView(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, format=None):
        """
        Get all account profile types
        e.g renter, landlord, agent
        """
        types = ProfileType.objects.all()
        serializer = ProfileTypeSerializer(types, many=True)
        return Response(serializer.data)
