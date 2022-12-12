from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from luvio_api.models import ProfileType
from luvio_api.serializers.profile_type_serializer import ProfileTypeSerializer


class ProfileTypeView(APIView):

    def get(self, request, format=None):
        """Get all existing accounts profile types

        Args:
            request (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        types = ProfileType.objects.all()
        serializer = ProfileTypeSerializer(types, many=True)
        return Response(serializer.data)
