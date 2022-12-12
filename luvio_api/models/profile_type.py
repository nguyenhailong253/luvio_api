from django.db import models


class ProfileType(models.Model):
    profile_type = models.CharField(max_length=10)

    class Meta:
        db_table = 'profile_types'
        managed = False

    def __str__(self):
        return self.profile_type
