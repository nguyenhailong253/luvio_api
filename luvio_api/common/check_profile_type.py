from rest_framework import exceptions

from luvio_api.models import ProfileType, UserProfile


def check_profile_type(profile_id: int, profile_type_name: str):
    profile = UserProfile.objects.get(pk=profile_id)
    profile_type = ProfileType.objects.get(profile_type=profile_type_name)
    if profile.profile_type != profile_type:
        raise exceptions.ValidationError({"message": "Incorrect profile type!"})
