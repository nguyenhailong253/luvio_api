from rest_framework import serializers

from luvio_api.models import LandlordProfilesAddresses


class LandlordProfilesAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfilesAddresses
        fields = "__all__"

    def create(self, validated_data: dict) -> LandlordProfilesAddresses:
        return LandlordProfilesAddresses.objects.create(**validated_data)
