from datetime import datetime

from django.db import models

from luvio_api.common.constants import DATE_FORMAT, TEXT_FIELD_MAX_LENGTH
from luvio_api.models import Address, ProfileType, UserAccount


class UserProfile(models.Model):
    """
    ManyToOne relationship with UserAccount - Each account can have multiple profiles (max 3 at the moment)
    ManyToOne relationship with ProfileType - There are multiple profiles of the same type
    """

    # Ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey.to_field
    # by default, use primary key of related object
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.CASCADE)
    avatar_link = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH, null=True, blank=True, default=None
    )
    profile_pitch = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH, null=True, blank=True, default=None
    )
    profile_url = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        unique=True,
    )
    # Could have used models.DateField(auto_now_add=True) ref: https://stackoverflow.com/a/51389274/8749888
    date_created = models.DateField(default=datetime.today().strftime(DATE_FORMAT))
    addresses = models.ManyToManyField(
        Address,
        through="ProfilesAddresses",
    )
