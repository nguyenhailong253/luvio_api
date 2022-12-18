from django.db import models
from django.contrib.auth.models import AbstractUser
from luvio_api.common.constants import INVALID_EMAIL, EMAIL_FIELD_MAX_LENGTH, NAME_FIELD_MAX_LENGTH, PASSWORD_MAX_LENGTH, PWD_SALT_MAX_LENGTH, AU_MOBILE_MAX_LENGTH

# Ref: https://docs.djangoproject.com/en/4.1/ref/contrib/auth/


class Registration(AbstractUser):
    # Ref: https://stackoverflow.com/questions/22586897/creating-custom-fields-with-django-allauth
    # Ref: https://stackoverflow.com/a/59310643
    REQUIRED_FIELDS = ('password', 'first_name', 'last_name',
                       'date_of_birth', 'username')
    # Ref: https://stackoverflow.com/questions/51308530/attributeerror-type-object-myuser-has-no-attribute-username-field
    USERNAME_FIELD = 'primary_email'

    # Ref: https://stackoverflow.com/a/67890255
    primary_email = models.EmailField(
        max_length=EMAIL_FIELD_MAX_LENGTH, default=INVALID_EMAIL, unique=True)
    username = models.CharField(
        max_length=EMAIL_FIELD_MAX_LENGTH, default=INVALID_EMAIL, unique=True)
    password = models.CharField(max_length=PASSWORD_MAX_LENGTH)
    first_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(
        max_length=AU_MOBILE_MAX_LENGTH, null=True, blank=True)


class UserAccount(models.Model):
    primary_email = models.EmailField(
        max_length=EMAIL_FIELD_MAX_LENGTH, unique=True)
    username = models.EmailField(
        max_length=EMAIL_FIELD_MAX_LENGTH, unique=True)
    password_hashed = models.CharField(max_length=PASSWORD_MAX_LENGTH)
    password_salt = models.CharField(max_length=PWD_SALT_MAX_LENGTH)
    first_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(
        max_length=AU_MOBILE_MAX_LENGTH, null=True, blank=True)

    class Meta:  # Ref: https://docs.djangoproject.com/en/4.1/ref/models/options/
        db_table = 'user_accounts'
        # Ref: https://stackoverflow.com/questions/16421574/database-table-names-with-django
        managed = False

    def __str__(self):
        return self.primary_email
