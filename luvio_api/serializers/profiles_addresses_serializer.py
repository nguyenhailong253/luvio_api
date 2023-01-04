import logging

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import (
    Address,
    ProfilesAddresses,
    StateAndTerritory,
    Suburb,
    UserProfile,
)

logger = logging.getLogger(DEFAULT_LOGGER)


class ProfilesAddressesCreateOrUpdateSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    display_address = serializers.CharField(max_length=320)
    unit_number = serializers.CharField(max_length=10, required=False, allow_null=True)
    street_number = serializers.CharField(max_length=20)
    street_name = serializers.CharField(max_length=100)
    street_type = serializers.CharField(max_length=50, required=False, allow_null=True)
    street_type_abbrev = serializers.CharField(
        max_length=10, required=False, allow_null=True
    )
    suburb = serializers.CharField(max_length=50)
    postcode = serializers.CharField(max_length=10)
    state = serializers.CharField(max_length=5)

    move_in_date = serializers.DateField(required=False, allow_null=True)
    move_out_date = serializers.DateField(required=False, allow_null=True)
    management_start_date = serializers.DateField(required=False, allow_null=True)
    management_end_date = serializers.DateField(required=False, allow_null=True)
    ownership_start_date = serializers.DateField(required=False, allow_null=True)
    ownership_end_date = serializers.DateField(required=False, allow_null=True)
    is_current_residence = serializers.BooleanField(default=False)

    def _get_address_from_payload(self, payload: dict) -> Address:
        """
        Get or create address from the info given in request payload
        """
        state = StateAndTerritory.objects.get(state_code=payload.pop("state"))
        suburb, created = Suburb.objects.get_or_create(
            state_and_territory=state,
            name=payload.pop("suburb"),
            postcode=payload.pop("postcode"),
        )
        logger.info(f"Suburb created? {created}: {suburb}")
        address, created = Address.objects.get_or_create(
            suburb=suburb,
            display_address=payload.pop("display_address"),
            unit_number=payload.pop("unit_number"),
            street_number=payload.pop("street_number"),
            street_name=payload.pop("street_name"),
            street_type=payload.pop("street_type"),
            street_type_abbrev=payload.pop("street_type_abbrev"),
        )
        logger.info(f"Address created? {created}: {address}")
        return address

    def _raise_conflict_error(self):
        """
        Return 409 Conflict HTTP response
        """
        res = serializers.ValidationError(
            {
                "message": "You cannot have the same address with the same start date more than once within one profile"
            },
        )
        res.status_code = status.HTTP_409_CONFLICT
        raise res

    def _check_duplicated_address_in_profile(
        self,
        profile: UserProfile,
        address: Address,
        profile_type_name: str,
        data: dict,
    ):
        """
        Upon creation of a new address linked to a profile, check if any other address
        in the same profile has the same start date or not
        """
        duplicated = False
        if profile_type_name == "tenant":
            duplicated = ProfilesAddresses.objects.filter(
                profile=profile,
                address=address,
                move_in_date=data.get("move_in_date", None),
            ).exists()
        elif profile_type_name == "agent":
            duplicated = ProfilesAddresses.objects.filter(
                profile=profile,
                address=address,
                management_start_date=data.get("management_start_date", None),
            ).exists()
        elif profile_type_name == "landlord":
            duplicated = ProfilesAddresses.objects.filter(
                profile=profile,
                address=address,
                ownership_start_date=data.get("ownership_start_date", None),
            ).exists()
        if duplicated:
            logger.error(
                f"Duplicated address and start date in the same profile. Profile id: {profile.id}"
            )
            self._raise_conflict_error()

    def _check_duplicated_address_in_profile_excluding_itself(
        self,
        profile: UserProfile,
        address: Address,
        profile_address: ProfilesAddresses,
        profile_type_name: str,
        data: dict,
    ):
        """
        Upon updating of an existing address linked to a profile, check if any other address
        in the same profile has the same start date or not, excluding the current address
        being updated
        """
        duplicated = False
        if profile_type_name == "tenant":
            duplicated = (
                ProfilesAddresses.objects.filter(
                    profile=profile,
                    address=address,
                    move_in_date=data.get("move_in_date", None),
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        elif profile_type_name == "agent":
            duplicated = (
                ProfilesAddresses.objects.filter(
                    profile=profile,
                    address=address,
                    management_start_date=data.get("management_start_date", None),
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        elif profile_type_name == "landlord":
            duplicated = (
                ProfilesAddresses.objects.filter(
                    profile=profile,
                    address=address,
                    ownership_start_date=data.get("ownership_start_date", None),
                )
                .exclude(pk=profile_address.id)
                .exists()
            )
        if duplicated:
            logger.error(
                f"Duplicated address and start date in the same profile. Profile id: {profile.id}, profile address id: {profile_address.id}"
            )
            self._raise_conflict_error()

    def create(self, validated_data: dict) -> ProfilesAddresses:
        """
        Create a link between an address and a profile
        """
        profile = get_object_or_404(UserProfile, pk=validated_data.pop("profile_id"))
        address = self._get_address_from_payload(validated_data)

        self._check_duplicated_address_in_profile(
            profile, address, profile.profile_type.profile_type, validated_data
        )
        return ProfilesAddresses.objects.create(
            **{
                **validated_data,
                "profile": profile,
                "address": address,
                "profile_type": profile.profile_type,
            }
        )

    def update(
        self, instance: ProfilesAddresses, validated_data: dict
    ) -> ProfilesAddresses:
        """
        Update current link between address and a profile
        """
        address = self._get_address_from_payload(validated_data)

        self._check_duplicated_address_in_profile_excluding_itself(
            instance.profile,
            address,
            instance,
            instance.profile_type.profile_type,
            validated_data,
        )
        instance.address = address
        instance.is_current_residence = validated_data.get(
            "is_current_residence", False
        )
        instance.move_in_date = validated_data.get("move_in_date", None)
        instance.move_out_date = validated_data.get("move_out_date", None)
        instance.management_start_date = validated_data.get(
            "management_start_date", None
        )
        instance.management_end_date = validated_data.get("management_end_date", None)
        instance.ownership_start_date = validated_data.get("ownership_start_date", None)
        instance.ownership_end_date = validated_data.get("ownership_end_date", None)
        instance.save()
        return instance
