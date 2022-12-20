from django.db import models


class ProfileType(models.Model):
    profile_type = models.CharField(max_length=10)

    def __str__(self):
        return self.profile_type
