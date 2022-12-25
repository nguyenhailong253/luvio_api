from django.db import models

from luvio_api.models import StateAndTerritory


class Suburb(models.Model):
    state_and_territory = models.ForeignKey(StateAndTerritory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.name
