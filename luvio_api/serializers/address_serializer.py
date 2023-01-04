from rest_framework import serializers

from luvio_api.models import Address


class AddressGetFullDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for when we want human-readable address (replace foreign keys with actual text)
    """

    postcode = serializers.SerializerMethodField()
    suburb = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    def get_postcode(self, address: Address) -> str:
        return address.suburb.postcode

    def get_suburb(self, address: Address) -> str:
        return address.suburb.name

    def get_state(self, address: Address) -> str:
        return address.suburb.state_and_territory.state_code

    class Meta:
        model = Address
        fields = [
            "display_address",
            "unit_number",
            "street_number",
            "street_name",
            "street_type",
            "street_type_abbrev",
            "suburb",
            "postcode",
            "state",
        ]
