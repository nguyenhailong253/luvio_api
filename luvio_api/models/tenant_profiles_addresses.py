from django.db import models

from luvio_api.models import Address, UserProfile


class TenantProfilesAddresses(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    move_in_date = models.DateField()
    move_out_date = models.DateField(null=True, blank=True)
    is_current_residence = models.BooleanField(default=False)
