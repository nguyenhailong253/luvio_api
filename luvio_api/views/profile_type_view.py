from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import ProfileType
from luvio_api.serializers import ProfileTypeSerializer


class ProfileTypeView(APIView):
    def get(self, request: Request):
        """
        Get all account profile types
        e.g renter, landlord, agent
        """
        types = ProfileType.objects.all()
        serializer = ProfileTypeSerializer(types, many=True)
        return Response(serializer.data)
