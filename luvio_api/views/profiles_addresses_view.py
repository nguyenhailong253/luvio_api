from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.common.check_profile_type import check_profile_type
from luvio_api.common.constants import (
    DOMAIN_API_PAYLOAD_FIELDS,
    PROFILE_ADDRESS_ID,
    PROFILE_TYPES,
    PROFILES_ADDRESSES_FIELD_MAPPINGS,
)
from luvio_api.common.domain_api_utils import (
    get_or_create_address,
    get_or_create_suburb,
)
from luvio_api.models import Address, StateAndTerritory, ProfilesAddresses
from luvio_api.serializers import ProfilesAddressesSerializer


class ProfilesAddressesView(APIView):
    def post(self, request: Request, profile_id: int) -> Response:
        """
        Link a new address to the current profile
        """
        check_profile_type(profile_id, PROFILE_TYPES["tenant"])
        state = self._get_state(request.data)
        address = self._get_address_from_payload(request.data, state)

        data = self._construct_new_profile_address(profile_id, address, request.data)

        if ProfilesAddresses.objects.filter(
            profile=profile_id, address=address, move_in_date=data["move_in_date"]
        ).exists():
            return Response(
                {
                    "message": "You cannot have the same address with the same move in date more than once within one profile"
                },
                status=status.HTTP_409_CONFLICT,
            )

        serializer = ProfilesAddressesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response(
            {
                "message": "Successfully linked address to current profile",
                PROFILE_ADDRESS_ID: record.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request: Request, profile_id: int) -> Response:
        """
        Update exisitng address on current profile
        """
        check_profile_type(profile_id, PROFILE_TYPES["tenant"])
        state = self._get_state(request.data)
        address = self._get_address_from_payload(request.data, state)

        profile_address = get_object_or_404(
            ProfilesAddresses, pk=request.data.get(PROFILE_ADDRESS_ID)
        )
        self._update_profile_address(profile_address, request.data, address)

        if (
            ProfilesAddresses.objects.filter(
                profile=profile_id,
                address=address,
                move_in_date=profile_address.move_in_date,
            )
            .exclude(pk=request.data.get(PROFILE_ADDRESS_ID))
            .exists()
        ):
            return Response(
                {
                    "message": "You cannot have the same address with the same move in date more than once within one profile"
                },
                status=status.HTTP_409_CONFLICT,
            )
        profile_address.save()
        return Response({"message": "Successfully updated address in current profile"})

    def delete(self, request: Request, profile_id: int) -> Response:
        """
        Delete an exisitng address on current profile
        """
        check_profile_type(profile_id, PROFILE_TYPES["tenant"])
        get_object_or_404(
            ProfilesAddresses, pk=request.data.get(PROFILE_ADDRESS_ID)
        ).delete()
        return Response({"message": "Successfully deleted address in current profile"})

    def _get_state(self, payload: dict) -> StateAndTerritory:
        return StateAndTerritory.objects.get(
            state_code=payload[DOMAIN_API_PAYLOAD_FIELDS["state"]]
        )

    def _get_address_from_payload(
        self, payload: dict, state: StateAndTerritory
    ) -> Address:
        suburb = get_or_create_suburb(payload, state)
        address = get_or_create_address(
            payload,
            suburb,
            payload[DOMAIN_API_PAYLOAD_FIELDS["display_address"]],
        )
        return address

    def _construct_new_profile_address(
        self, profile_id: int, address: Address, payload: dict
    ):
        return {
            "profile": profile_id,
            "address": address.id,
            "move_in_date": payload[
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_in_date"]
            ],
            "move_out_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_out_date"], None
            ),
            "is_current_residence": payload[
                PROFILES_ADDRESSES_FIELD_MAPPINGS["is_current_residence"]
            ],
        }

    def _update_profile_address(
        self, profile_address: ProfilesAddresses, payload: dict, address: Address
    ):
        profile_address.address = address
        profile_address.move_in_date = payload.get(
            PROFILES_ADDRESSES_FIELD_MAPPINGS["move_in_date"],
            profile_address.move_in_date,
        )
        profile_address.move_out_date = payload.get(
            PROFILES_ADDRESSES_FIELD_MAPPINGS["move_out_date"],
            profile_address.move_out_date,
        )
        profile_address.is_current_residence = payload.get(
            PROFILES_ADDRESSES_FIELD_MAPPINGS["is_current_residence"],
            profile_address.is_current_residence,
        )
