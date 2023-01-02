import logging

from rest_framework import serializers, status

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import UserProfile
from luvio_api.serializers import AddressGetFullDetailSerializer

logger = logging.getLogger(DEFAULT_LOGGER)


class UserProfileCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def create(self, validated_data: dict) -> UserProfile:
        if UserProfile.objects.filter(
            profile_type=validated_data.get("profile_type"),
            account=validated_data.get("account"),
        ).exists():
            logger.error(
                f"Failed to create a new profile because this profile type already exists in this account. Username = {validated_data.get('account')}"
            )
            res = serializers.ValidationError(
                {
                    "message": f"This account already has a profile with {validated_data.get('profile_type')} profile type"
                },
            )
            res.status_code = (
                status.HTTP_409_CONFLICT
            )  # Ref: https://stackoverflow.com/a/63211074/8749888
            raise res
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
