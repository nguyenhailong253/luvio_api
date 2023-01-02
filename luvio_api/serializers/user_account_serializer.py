from rest_framework import serializers

from luvio_api.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"

    def create(self, validated_data: dict) -> UserAccount:
        # Ref: https://stackoverflow.com/a/63976118/8749888
        raw_password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(raw_password)
        user.save()
        return user

    def update(self, instance: UserAccount, validated_data: dict) -> UserAccount:
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.date_of_birth = validated_data.get("date_of_birth", None)
        instance.mobile = validated_data.get("mobile", None)
        instance.save()
        return instance
