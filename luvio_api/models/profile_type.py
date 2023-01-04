from django.db import models


class ProfileType(models.Model):
    """
    Each user can have an account, each account can have 3 profiles max, 1 for each type
    Currently the 3 types are: landlord, agent, and tenant
    """

    profile_type = models.CharField(max_length=10)

    def __str__(self):
        return self.profile_type
