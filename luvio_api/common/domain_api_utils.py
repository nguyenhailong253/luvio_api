from luvio_api.models import Address, StateAndTerritory, Suburb


def store_suburb_and_address_data(addresses: list):
    """
    Store all addresses data retrieved from Domain API to our own DB
    """
    for address in addresses:
        display_address = address["address"]
        details = address["addressComponents"]

        state = StateAndTerritory.objects.get(state_code=details["state"])
        suburb = get_or_create_suburb(details, state)
        get_or_create_address(details, suburb, display_address)


def get_or_create_suburb(address_details: dict, state: StateAndTerritory):
    """
    Check if suburb data for an address already exists, if not create new entry in our DB
    """
    if Suburb.objects.filter(
        state_and_territory=state,
        name=address_details["suburb"],
        postcode=address_details["postCode"],
    ).exists():
        return Suburb.objects.get(
            state_and_territory=state,
            name=address_details["suburb"],
            postcode=address_details["postCode"],
        )
    return Suburb.objects.create(
        state_and_territory=state,
        name=address_details["suburb"],
        postcode=address_details["postCode"],
    )


def get_or_create_address(address_details: dict, suburb: Suburb, display_address: str):
    """
    Check if address data already exists, if not create new entry in our DB
    """
    if Address.objects.filter(
        suburb=suburb,
        unit_number=address_details["unitNumber"],
        street_number=address_details["streetNumber"],
        street_name=address_details["streetName"],
        street_type=address_details["streetTypeLong"],
        street_type_abbrev=address_details["streetType"],
    ).exists():
        return Address.objects.get(
            suburb=suburb,
            unit_number=address_details["unitNumber"],
            street_number=address_details["streetNumber"],
            street_name=address_details["streetName"],
            street_type=address_details["streetTypeLong"],
            street_type_abbrev=address_details["streetType"],
        )
    return Address.objects.create(
        suburb=suburb,
        display_address=display_address,
        unit_number=address_details["unitNumber"],
        street_number=address_details["streetNumber"],
        street_name=address_details["streetName"],
        street_type=address_details["streetTypeLong"],
        street_type_abbrev=address_details["streetType"],
    )
