from django.db import models

from luvio_api.models import Suburb


class Address(models.Model):
    # OneToOne vs ForeighKey (aka ManyToOne) https://stackoverflow.com/a/26937468/8749888
    suburb = models.ForeignKey(Suburb, on_delete=models.CASCADE)
    display_address = models.CharField(max_length=320)
    unit_number = models.CharField(max_length=10, null=True, blank=True)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    street_type = models.CharField(max_length=50, null=True, blank=True)
    street_type_abbrev = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.display_address
