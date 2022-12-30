from typing import Any, Iterable

from luvio_api.models import Address, StateAndTerritory, Suburb


def convert_address_suggestion_fields_to_snake_case(
    addresses: Iterable[Any],
) -> Iterable[Any]:
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


def store_suburb_and_address_data(addresses: Iterable[Any]):
    """
    Store all addresses data retrieved from Domain API to our own DB
    """
    for address in addresses:
        state = StateAndTerritory.objects.get(state_code=address["state"])
        suburb = get_or_create_suburb(address, state)
        get_or_create_address(address, suburb)


def get_or_create_suburb(address: dict, state: StateAndTerritory) -> Suburb:
    """
    Check if suburb data for an address already exists, if not create new entry in our DB
    """
    if Suburb.objects.filter(
        state_and_territory=state,
        name=address["suburb"],
        postcode=address["postcode"],
    ).exists():
        return Suburb.objects.get(
            state_and_territory=state,
            name=address["suburb"],
            postcode=address["postcode"],
        )
    return Suburb.objects.create(
        state_and_territory=state,
        name=address["suburb"],
        postcode=address["postcode"],
    )


def get_or_create_address(address: dict, suburb: Suburb) -> Address:
    """
    Check if address data already exists, if not create new entry in our DB
    """
    if Address.objects.filter(
        suburb=suburb,
        unit_number=address["unit_number"],
        street_number=address["street_number"],
        street_name=address["street_name"],
        street_type=address["street_type"],
        street_type_abbrev=address["street_type_abbrev"],
    ).exists():
        return Address.objects.get(
            suburb=suburb,
            unit_number=address["unit_number"],
            street_number=address["street_number"],
            street_name=address["street_name"],
            street_type=address["street_type"],
            street_type_abbrev=address["street_type_abbrev"],
        )
    return Address.objects.create(
        suburb=suburb,
        display_address=address["display_address"],
        unit_number=address["unit_number"],
        street_number=address["street_number"],
        street_name=address["street_name"],
        street_type=address["street_type"],
        street_type_abbrev=address["street_type_abbrev"],
    )
