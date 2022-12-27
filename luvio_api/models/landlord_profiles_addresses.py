from django.db import models

from luvio_api.models import Address, UserProfile


class LandlordProfilesAddresses(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ownership_start_date = models.DateField()
    ownership_end_date = models.DateField(null=True, blank=True)
    is_current_residence = models.BooleanField(default=False)
