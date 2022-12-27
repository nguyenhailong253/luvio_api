from rest_framework import serializers

from luvio_api.models import AgentProfilesAddresses


class AgentProfilesAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfilesAddresses
        fields = "__all__"

    def create(self, validated_data: dict) -> AgentProfilesAddresses:
        return AgentProfilesAddresses.objects.create(**validated_data)
