from django.db import models

from luvio_api.models import Address, ProfileType, UserProfile


class ProfilesAddresses(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.CASCADE)
    move_in_date = models.DateField(null=True, blank=True, default=None)
    move_out_date = models.DateField(null=True, blank=True, default=None)
    management_start_date = models.DateField(null=True, blank=True, default=None)
    management_end_date = models.DateField(null=True, blank=True, default=None)
    ownership_start_date = models.DateField(null=True, blank=True, default=None)
    ownership_end_date = models.DateField(null=True, blank=True, default=None)
    is_current_residence = models.BooleanField(default=False)
