import logging

from rest_framework import serializers

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import UserProfile
from luvio_api.serializers import AddressGetFullDetailSerializer

logger = logging.getLogger(DEFAULT_LOGGER)


class PublicUserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Custom serializer for getting full details of a profile which is publicly accessible
    Including full list of serialized addresses, and employment details, etc
    """

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
            "avatar",
            "profile_pitch",
            "profile_uri",
            "date_created",
            "addresses",
        ]
