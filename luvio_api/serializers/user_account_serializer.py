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
        self.verify_username_and_email(
            validated_data['username'], validated_data['primary_email'])
        salt = bcrypt.gensalt(rounds=COST_FACTOR)
        hashed_pwd = bcrypt.hashpw(
            validated_data['password'].encode('utf-8'), salt)
        user = UserAccount(
            primary_email=validated_data['primary_email'],
            username=validated_data['username'],
            # Ref: https://stackoverflow.com/a/38262440
            password_hashed=hashed_pwd.decode('utf-8'),
            password_salt=salt.decode('utf-8'),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            mobile=validated_data['mobile']
        )
        user.save()
        return user

    def verify_username_and_email(self, username, email):
        if UserAccount.objects.filter(primary_email=email).exists():
            raise exceptions.ValidationError(
                {"message": "This email is already used for another account! Please use a different email address"}, code=400)
        if UserAccount.objects.filter(username=username).exists():
            raise exceptions.ValidationError(
                {"message": "This username is already used for another account! Please use a different username"}, code=400)


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = '__all__'
