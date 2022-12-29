from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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
from luvio_api.models import Address, ProfilesAddresses, StateAndTerritory, UserProfile
from luvio_api.serializers import ProfilesAddressesSerializer


class ProfilesAddressesListView(APIView):
    def post(self, request: Request, profile_id: int) -> Response:
        """
        Link a new address to the current profile
        """
        state = get_state(request.data)
        address = get_address_from_payload(request.data, state)
        profile_type = get_object_or_404(UserProfile, pk=profile_id).profile_type
        print(
            f"profile type: {profile_type}, id: {profile_type.id}, name: {profile_type.profile_type}"
        )

        data = self._construct_new_profile_address(
            profile_id, address, request.data, profile_type.id
        )

        if self._has_duplicated_address_in_profile(
            profile_id, address, data, profile_type.profile_type
        ):
            return Response(
                {
                    "message": "You cannot have the same address with the same start date more than once within one profile"
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

    def _construct_new_profile_address(
        self, profile_id: int, address: Address, payload: dict, profile_type_id: str
    ):
        return {
            "profile": profile_id,
            "address": address.id,
            "profile_type": profile_type_id,
            "move_in_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_in_date"], None
            ),
            "move_out_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_out_date"], None
            ),
            "management_start_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["management_start_date"], None
            ),
            "management_end_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["management_end_date"], None
            ),
            "ownership_start_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["ownership_start_date"], None
            ),
            "ownership_end_date": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["ownership_end_date"], None
            ),
            "is_current_residence": payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["is_current_residence"], False
            ),
        }

    def _has_duplicated_address_in_profile(
        self, profile_id: int, address: Address, data: dict, profile_type_name: str
    ) -> bool:
        if profile_type_name == "tenant":
            return ProfilesAddresses.objects.filter(
                profile=profile_id, address=address, move_in_date=data["move_in_date"]
            ).exists()
        if profile_type_name == "agent":
            return ProfilesAddresses.objects.filter(
                profile=profile_id,
                address=address,
                management_start_date=data["management_start_date"],
            ).exists()
        if profile_type_name == "landlord":
            return ProfilesAddresses.objects.filter(
                profile=profile_id,
                address=address,
                ownership_start_date=data["ownership_start_date"],
            ).exists()
        raise exceptions.ValidationError({"message": "Invalid profile type!"})


class ProfilesAddressesDetailView(APIView):
    def put(
        self, request: Request, profile_id: int, profile_address_id: int
    ) -> Response:
        """
        Update exisitng address on current profile
        """
        state = get_state(request.data)
        address = get_address_from_payload(request.data, state)

        profile_address = get_object_or_404(
            ProfilesAddresses, pk=profile_address_id, profile=profile_id
        )
        self._update_profile_address(profile_address, request.data, address)

        if self._has_duplicated_address_in_profile(profile_address):
            return Response(
                {
                    "message": "You cannot have the same address with the same start date more than once within one profile"
                },
                status=status.HTTP_409_CONFLICT,
            )
        profile_address.save()
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

    def _has_duplicated_address_in_profile(
        self, profile_address: ProfilesAddresses
    ) -> bool:
        if profile_address.profile_type.profile_type == "tenant":
            return (
                ProfilesAddresses.objects.filter(
                    profile=profile_address.profile,
                    address=profile_address.address,
                    move_in_date=profile_address.move_in_date,
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        if profile_address.profile_type.profile_type == "agent":
            return (
                ProfilesAddresses.objects.filter(
                    profile=profile_address.profile,
                    address=profile_address.address,
                    management_start_date=profile_address.management_start_date,
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        if profile_address.profile_type.profile_type == "landlord":
            return (
                ProfilesAddresses.objects.filter(
                    profile=profile_address.profile,
                    address=profile_address.address,
                    ownership_start_date=profile_address.ownership_start_date,
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        raise exceptions.ValidationError({"message": "Invalid profile type!"})

    def _update_profile_address(
        self, profile_address: ProfilesAddresses, payload: dict, address: Address
    ):
        profile_address.address = address
        profile_address.is_current_residence = payload.get(
            PROFILES_ADDRESSES_FIELD_MAPPINGS["is_current_residence"],
            profile_address.is_current_residence,
        )
        if profile_address.profile_type.profile_type == "tenant":
            profile_address.move_in_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_in_date"], None
            )
            profile_address.move_out_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["move_out_date"], None
            )
        if profile_address.profile_type.profile_type == "agent":
            profile_address.management_start_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["management_start_date"], None
            )
            profile_address.management_end_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["management_end_date"], None
            )
        if profile_address.profile_type.profile_type == "landlord":
            profile_address.ownership_start_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["ownership_start_date"], None
            )
            profile_address.ownership_end_date = payload.get(
                PROFILES_ADDRESSES_FIELD_MAPPINGS["ownership_end_date"], None
            )


def get_state(payload: dict) -> StateAndTerritory:
    return StateAndTerritory.objects.get(
        state_code=payload[DOMAIN_API_PAYLOAD_FIELDS["state"]]
    )


def get_address_from_payload(payload: dict, state: StateAndTerritory) -> Address:
    suburb = get_or_create_suburb(payload, state)
    address = get_or_create_address(
        payload,
        suburb,
        payload[DOMAIN_API_PAYLOAD_FIELDS["display_address"]],
    )
    return address
