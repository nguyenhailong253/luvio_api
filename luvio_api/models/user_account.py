from django.db import models


class UserAccount(models.Model):
    primary_email = models.EmailField(max_length=320, unique=True)
    username = models.EmailField(max_length=320, unique=True)
    password_hashed = models.CharField(max_length=200)
    password_salt = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)

    class Meta:  # Ref: https://docs.djangoproject.com/en/4.1/ref/models/options/
        db_table = 'user_accounts'
        # Ref: https://stackoverflow.com/questions/16421574/database-table-names-with-django
        managed = False

    def __str__(self):
        return self.username
