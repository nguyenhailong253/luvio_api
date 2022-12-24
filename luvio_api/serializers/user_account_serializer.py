from rest_framework import serializers

from luvio_api.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"

    def create(self, validated_data: dict):
        # Ref: https://stackoverflow.com/a/63976118/8749888
        raw_password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(raw_password)
        user.save()
        return user
