import logging

from rest_framework import serializers, status

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import ProfileType, UserAccount, UserProfile
from luvio_api.serializers import AddressGetFullDetailSerializer

logger = logging.getLogger(DEFAULT_LOGGER)


class UserProfileCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def _is_account_already_has_profile(
        self, account: UserAccount, profile_type: ProfileType
    ):
        """
        Upon creation of a profile, check if this account already has a profile of the
        same type or not. Each account can only have 1 profile of each type, i.e 3 profiles
        maximum
        """
        if UserProfile.objects.filter(
            profile_type=profile_type,
            account=account,
        ).exists():
            logger.error(
                f"Failed to create a new profile because this profile type already exists in this account. Username = {account}"
            )
            res = serializers.ValidationError(
                {
                    "message": f"This account already has a profile with {profile_type} profile type"
                },
            )
            res.status_code = (
                status.HTTP_409_CONFLICT
            )  # Ref: https://stackoverflow.com/a/63211074/8749888
            raise res

    def create(self, validated_data: dict) -> UserProfile:
        """
        Create a new profile based on the profile type
        """
        self._is_account_already_has_profile(
            validated_data.get("account"), validated_data.get("profile_type")  # type: ignore[arg-type]
        )
        return UserProfile.objects.create(**validated_data)

    def update(self, instance: UserProfile, validated_data: dict) -> UserProfile:
        """
        Update an existing profile - but we can only update 2 fields currently
        """
        instance.avatar_link = validated_data.get("avatar_link", None)
        instance.profile_pitch = validated_data.get("profile_pitch", None)
        instance.save()
        return instance


class UserProfileListSerializer(serializers.ModelSerializer):
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, profile: UserProfile) -> str:
        """
        Get the profile type NAME instead of just primary key
        """
        return profile.profile_type.profile_type

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "avatar_link",
            "profile_pitch",
            "profile_url",
            "date_created",
            "profile_type",
        ]


class UserProfileGetFullDetailSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, profile: UserProfile) -> str:
        """
        Get the profile type NAME instead of just primary key
        """
        return profile.profile_type.profile_type

    def get_addresses(self, profile: UserProfile) -> list:
        """
        Get the addresses, with suburb name instead of foreign key, postcode, state name,
        and all relevant details about start/end dates from the profile_address_relation
        (through/joint table)
        """
        # Ref: https://stackoverflow.com/a/6019587/8749888
        profilesaddresses = profile.profilesaddresses_set.all()
        addresses = AddressGetFullDetailSerializer(
            [pa.address for pa in profilesaddresses], many=True, read_only=True
        ).data
        for index in range(0, len(addresses)):
            address = addresses[index]
            profileaddress = profilesaddresses[index]
            address["ownership_start_date"] = profileaddress.ownership_start_date
            address["ownership_end_date"] = profileaddress.ownership_end_date
            address["move_in_date"] = profileaddress.move_in_date
            address["move_out_date"] = profileaddress.move_out_date
            address["management_start_date"] = profileaddress.management_start_date
            address["management_end_date"] = profileaddress.management_end_date
            address["is_current_residence"] = profileaddress.is_current_residence
            address["profile_address_relation_id"] = profileaddress.id
        return addresses

    class Meta:
        model = UserProfile
        fields = [
            "profile_type",
            "avatar_link",
            "profile_pitch",
            "profile_url",
            "date_created",
            "addresses",
        ]
