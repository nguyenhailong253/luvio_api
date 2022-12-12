from rest_framework import serializers
from luvio_api.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

    def save(self):
        """Save user account
        """
        # validate username password
        # salt hash
        # save
