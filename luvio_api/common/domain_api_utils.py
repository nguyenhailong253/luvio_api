import logging
from typing import Any, Iterable

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import Address, StateAndTerritory, Suburb

logger = logging.getLogger(DEFAULT_LOGGER)


def convert_address_suggestion_fields_to_snake_case(
    addresses: Iterable[Any],
) -> Iterable[Any]:
    """
    Convert list of addresses with properties in camelCase (from frontend or from Domain API)
    to snake case to follow python convention
    """
    converted_addresses = []
    for address in addresses:
        converted_address = {
            "display_address": address["address"],
            "unit_number": address["addressComponents"]["unitNumber"],
            "street_number": address["addressComponents"]["streetNumber"],
            "street_name": address["addressComponents"]["streetName"],
            "street_type": address["addressComponents"]["streetTypeLong"],
            "street_type_abbrev": address["addressComponents"]["streetType"],
            "suburb": address["addressComponents"]["suburb"],
            "postcode": address["addressComponents"]["postCode"],
            "state": address["addressComponents"]["state"],
        }
        converted_addresses.append(converted_address)
    return converted_addresses


def store_suburb_and_address_data(addresses: Iterable[dict]):
    """
    Store all addresses data retrieved from Domain API to our own DB
    """
    for address in addresses:
        state = StateAndTerritory.objects.get(state_code=address["state"])
        suburb, created = Suburb.objects.get_or_create(
            state_and_territory=state,
            name=address["suburb"],
            postcode=address["postcode"],
        )
        logger.info(f"Suburb created? {created}: {suburb}")
        address, created = Address.objects.get_or_create(
            suburb=suburb,
            display_address=address["display_address"],
            unit_number=address["unit_number"],
            street_number=address["street_number"],
            street_name=address["street_name"],
            street_type=address["street_type"],
            street_type_abbrev=address["street_type_abbrev"],
        )
        logger.info(f"Address created? {created}: {address}")
