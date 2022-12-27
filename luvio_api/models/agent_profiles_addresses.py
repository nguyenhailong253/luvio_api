from django.db import models

from luvio_api.models import Address, UserProfile


class AgentProfilesAddresses(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    management_start_date = models.DateField()
    management_end_date = models.DateField(null=True, blank=True)
