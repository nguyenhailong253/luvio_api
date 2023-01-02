from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import ProfilesAddresses
from luvio_api.serializers import ProfilesAddressesCreateOrUpdateSerializer


class ProfilesAddressesListView(APIView):
    def post(self, request: Request, profile_id: int) -> Response:
        """
        Link a new address to the current profile
        """
        serializer = ProfilesAddressesCreateOrUpdateSerializer(
            data={**request.data, "profile_id": profile_id}
        )
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response(
            {
                "message": "Successfully linked address to current profile",
                "profile_address_id": record.id,
            },
            status=status.HTTP_201_CREATED,
        )


class ProfilesAddressesDetailView(APIView):
    def put(
        self, request: Request, profile_id: int, profile_address_id: int
    ) -> Response:
        """
        Update exisitng address on current profile
        """
        profile_address = get_object_or_404(
            ProfilesAddresses, pk=profile_address_id, profile=profile_id
        )
        serializer = ProfilesAddressesCreateOrUpdateSerializer(
            profile_address,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully updated address in current profile"})

    def delete(
        self, request: Request, profile_id: int, profile_address_id: int
    ) -> Response:
        """
        Delete an exisitng address on current profile
        """
        get_object_or_404(
            ProfilesAddresses, pk=profile_address_id, profile=profile_id
        ).delete()
        return Response({"message": "Successfully deleted address in current profile"})
