from rest_framework import serializers

from luvio_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # Ref: https://stackoverflow.com/a/39137996/8749888
    # Ref: https://stackoverflow.com/a/50999209/8749888
    # Ref: https://www.django-rest-framework.org/api-guide/relations/#slugrelatedfield
    # profile_type = serializers.SlugRelatedField(
    #     queryset=ProfileType.objects.all(), slug_field="profile_type"
    # )

    class Meta:
        model = UserProfile
        fields = "__all__"
