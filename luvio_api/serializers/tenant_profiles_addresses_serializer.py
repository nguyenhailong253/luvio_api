from rest_framework import serializers

from luvio_api.models import TenantProfilesAddresses


class TenantProfilesAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfilesAddresses
        fields = "__all__"

    def create(self, validated_data: dict):
        return TenantProfilesAddresses.objects.create(**validated_data)
