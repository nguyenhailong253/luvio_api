from django.contrib.auth.models import AbstractUser
from django.db import models

from luvio_api.common.constants import (
    AU_MOBILE_MAX_LENGTH,
    EMAIL_FIELD_MAX_LENGTH,
    NAME_FIELD_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
)

# Ref: https://docs.djangoproject.com/en/4.1/ref/contrib/auth/


class UserAccount(AbstractUser):
    # Ref: https://stackoverflow.com/questions/22586897/creating-custom-fields-with-django-allauth
    # Ref: https://stackoverflow.com/a/59310643
    REQUIRED_FIELDS = (
        "email",
        "password",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_active",
    )
    # Ref: https://stackoverflow.com/questions/51308530/attributeerror-type-object-myuser-has-no-attribute-username-field
    USERNAME_FIELD = "username"

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_FIELD_MAX_LENGTH, unique=True)
    username = models.CharField(max_length=EMAIL_FIELD_MAX_LENGTH, unique=True)
    password = models.CharField(max_length=PASSWORD_MAX_LENGTH)
    first_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=AU_MOBILE_MAX_LENGTH, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
