import bcrypt

from rest_framework import serializers, exceptions
from luvio_api.models import UserAccount, Registration

# Ref: https://codecurated.com/blog/how-to-better-store-password-in-database/
# Ref: https://zetcode.com/python/bcrypt/
# Ref: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
COST_FACTOR = 12  # about 213ms to generate salt


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data: dict):
        """
        Create new user account
        """
        if UserAccount.objects.filter(primary_email=validated_data['primary_email']).exists():
            raise exceptions.ValidationError(
                {"message": "This email is already used for another account! Please use a different email address"}, code=400)
        salt = bcrypt.gensalt(rounds=COST_FACTOR)
        print(f"Salt: {salt}")
        hashed_pwd = bcrypt.hashpw(
            validated_data['password'].encode('utf-8'), salt)
        print(f"Hashed pwd: {hashed_pwd}")
        user = UserAccount(
            primary_email=validated_data['primary_email'],
            password_hashed=hashed_pwd,
            password_salt=salt,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            mobile=validated_data['mobile']
        )
        user.save()
        return user


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = '__all__'
