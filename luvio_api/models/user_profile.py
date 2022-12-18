from django.db import models
from luvio_api.common.constants import TEXT_FIELD_MAX_LENGTH

class UserProfile(models.Model):
    account_id = models.BigIntegerField()
    profile_type = models.BigIntegerField()
    avatar_link = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH)
    profile_pitch = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH)
    profile_url = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH)

    class Meta:
        db_table = 'user_profiles'
        managed = False
