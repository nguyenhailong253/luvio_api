from rest_framework import serializers

from luvio_api.models import ProfilesAddresses


class ProfilesAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilesAddresses
        fields = "__all__"

    def create(self, validated_data: dict) -> ProfilesAddresses:
        return ProfilesAddresses.objects.create(**validated_data)
