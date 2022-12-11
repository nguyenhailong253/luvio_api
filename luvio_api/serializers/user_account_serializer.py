from rest_framework import serializers
from luvio_api.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'password_hashed', 'password_salt', 'first_name',
                  'last_name', 'date_of_birth', 'primary_email', 'secondary_email', 'mobile']
