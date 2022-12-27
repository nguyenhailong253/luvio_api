INVALID_EMAIL = "invalidemail"
TEXT_FIELD_MAX_LENGTH = 3000
EMAIL_FIELD_MAX_LENGTH = 320
NAME_FIELD_MAX_LENGTH = 100
PASSWORD_MAX_LENGTH = 320
PWD_SALT_MAX_LENGTH = 200
AU_MOBILE_MAX_LENGTH = 10


DOMAIN_API_PAYLOAD_FIELDS = {
    "display_address": "address",
    "unit_number": "unitNumber",
    "street_number": "streetNumber",
    "street_name": "streetName",
    "street_type": "streetTypeLong",
    "street_type_abbrev": "streetType",
    "suburb": "suburb",
    "postcode": "postCode",
    "state": "state",
}

TENANT_PROFILES_ADDRESSES_FIELD_MAPPINGS = {
    "move_in_date": "moveInDate",
    "move_out_date": "moveOutDate",
    "is_current_residence": "isCurrentResidence",
}

AGENT_PROFILES_ADDRESSES_FIELD_MAPPINGS = {
    "management_start_date": "managementStartDate",
    "management_end_date": "managementEndDate",
}

PROFILE_ADDRESS_ID = "profileAddressId"

PROFILE_TYPES = {
    "tenant": "tenant",
    "agent": "agent",
    "landlord": "landlord",
}
