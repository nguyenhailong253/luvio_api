from rest_framework import serializers

from luvio_api.models import UserProfile, UserAccount
from luvio_api.serializers import AddressGetFullDetailSerializer


class UserProfileCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

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
