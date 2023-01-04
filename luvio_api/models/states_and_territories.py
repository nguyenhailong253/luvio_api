from django.db import models


class StateAndTerritory(models.Model):
    """
    Currently store Australian states only.
    But this is intentionally named as states AND territory for future expansion
    """

    state_code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.name
