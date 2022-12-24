import bcrypt
from rest_framework import exceptions, serializers

from luvio_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
