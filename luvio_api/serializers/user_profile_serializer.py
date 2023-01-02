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

    def is_account_already_has_profile(
        self, account: UserAccount, profile_type: ProfileType
    ):
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
        self.is_account_already_has_profile(
            validated_data.get("account"), validated_data.get("profile_type")  # type: ignore[arg-type]
        )
        return UserProfile.objects.create(**validated_data)

    def update(self, instance: UserProfile, validated_data: dict) -> UserProfile:
        instance.avatar_link = validated_data.get("avatar_link", None)
        instance.profile_pitch = validated_data.get("profile_pitch", None)
        instance.save()
        return instance


class UserProfileListSerializer(serializers.ModelSerializer):
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, profile: UserProfile) -> str:
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
    addresses = AddressGetFullDetailSerializer(many=True, read_only=True)
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, profile: UserProfile) -> str:
        return profile.profile_type.profile_type

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
