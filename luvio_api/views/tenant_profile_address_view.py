from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.common.constants import (
    DOMAIN_API_PAYLOAD_FIELDS,
    TENANT_PROFILES_ADDRESSES_FIELD_MAPPINGS,
)
from luvio_api.models import Address, StateAndTerritory, Suburb, TenantProfilesAddresses
from luvio_api.serializers import TenantProfilesAddressesSerializer


class TenantProfilesAddressesView(APIView):
    def post(self, request: Request, profile_id: int):
        """
        Link a new address to the current profile
        """
        state = StateAndTerritory.objects.get(
            state_code=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["state"])
        )

        if Suburb.objects.filter(
            state_and_territory=state,
            name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["suburb"]),
            postcode=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["postcode"]),
        ).exists():
            suburb = Suburb.objects.get(
                state_and_territory=state,
                name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["suburb"]),
                postcode=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["postcode"]),
            )
        else:
            suburb = Suburb.objects.create(
                state_and_territory=state,
                name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["suburb"]),
                postcode=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["postcode"]),
            )

        if Address.objects.filter(
            suburb=suburb,
            unit_number=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["unit_number"]),
            street_number=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_number"]),
            street_name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_name"]),
            street_type=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_type"]),
            street_type_abbrev=request.data.get(
                DOMAIN_API_PAYLOAD_FIELDS["street_type_abbrev"]
            ),
        ).exists():
            address = Address.objects.get(
                suburb=suburb,
                unit_number=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["unit_number"]),
                street_number=request.data.get(
                    DOMAIN_API_PAYLOAD_FIELDS["street_number"]
                ),
                street_name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_name"]),
                street_type=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_type"]),
                street_type_abbrev=request.data.get(
                    DOMAIN_API_PAYLOAD_FIELDS["street_type_abbrev"]
                ),
            )
        else:
            address = Address.objects.create(
                suburb=suburb,
                display_address=request.data.get(
                    DOMAIN_API_PAYLOAD_FIELDS["display_address"]
                ),
                unit_number=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["unit_number"]),
                street_number=request.data.get(
                    DOMAIN_API_PAYLOAD_FIELDS["street_number"]
                ),
                street_name=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_name"]),
                street_type=request.data.get(DOMAIN_API_PAYLOAD_FIELDS["street_type"]),
                street_type_abbrev=request.data.get(
                    DOMAIN_API_PAYLOAD_FIELDS["street_type_abbrev"]
                ),
            )
        data = {
            "profile": profile_id,
            "address": address.id,
            "move_in_date": request.data.get(
                TENANT_PROFILES_ADDRESSES_FIELD_MAPPINGS["move_in_date"]
            ),
            "move_out_date": request.data.get(
                TENANT_PROFILES_ADDRESSES_FIELD_MAPPINGS["move_out_date"], None
            ),
            "is_current_residence": request.data.get(
                TENANT_PROFILES_ADDRESSES_FIELD_MAPPINGS["is_current_residence"]
            ),
        }

        if TenantProfilesAddresses.objects.filter(
            profile=profile_id, address=address, move_in_date=data["move_in_date"]
        ).exists():
            return Response(
                {
                    "message": "You cannot have the same address with the same move in date more than once within one profile"
                },
                status=status.HTTP_409_CONFLICT,
            )

        serializer = TenantProfilesAddressesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully linked address to current profile"},
            status=status.HTTP_201_CREATED,
        )
