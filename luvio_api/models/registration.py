from django.db import models


class Registration(models.Model):
    primary_email = models.CharField(max_length=320)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=10, null=True)
