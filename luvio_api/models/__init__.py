# https://stackoverflow.com/a/47740087
from .profile_type import ProfileType
from .states_and_territories import StateAndTerritory
from .suburbs import Suburb
from .user_account import UserAccount
from .addresses import (
    Address,
)  # need to be imported after Suburb, otherwise circular import error
from .user_profile import UserProfile  # import after Address
from .profiles_addresses import ProfilesAddresses
