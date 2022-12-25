from django.db import models


class StateAndTerritory(models.Model):
    state_code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.name
