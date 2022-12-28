from django.db import models

from luvio_api.models import Address, UserProfile, ProfileType


class ProfilesAddresses(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.CASCADE)
    move_in_date = models.DateField(null=True, blank=True)
    move_out_date = models.DateField(null=True, blank=True)
    management_start_date = models.DateField(null=True, blank=True)
    management_end_date = models.DateField(null=True, blank=True)
    ownership_start_date = models.DateField(null=True, blank=True)
    ownership_end_date = models.DateField(null=True, blank=True)
    is_current_residence = models.BooleanField(default=False)
