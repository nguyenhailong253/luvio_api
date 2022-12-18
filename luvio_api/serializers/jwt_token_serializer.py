from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JwtTokenSerializer(TokenObtainPairSerializer):
    # Ref: https://stackoverflow.com/a/49221349
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.primary_email
        token['user_id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
