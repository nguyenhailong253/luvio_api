from django.db import models

from luvio_api.common.constants import TEXT_FIELD_MAX_LENGTH
from luvio_api.models import ProfileType, UserAccount


class UserProfile(models.Model):
    # Ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey.to_field
    # by default, use primary key of related object
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.CASCADE)
    avatar_link = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH, null=True, blank=True)
    profile_pitch = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH, null=True, blank=True)
    profile_url = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH, null=True, blank=True)

    def __str__(self):
        return self.profile_url
