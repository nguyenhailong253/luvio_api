from rest_framework import serializers

from luvio_api.models import ProfileType


class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileType()
        fields = '__all__'
