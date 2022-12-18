from django.db import models
from django.contrib.auth.models import AbstractUser
from luvio_api.common.constants import INVALID_EMAIL


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
        max_length=320, default=INVALID_EMAIL, unique=True)
    username = models.CharField(
        max_length=320, default=INVALID_EMAIL, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
