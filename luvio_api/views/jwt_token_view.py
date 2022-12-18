import bcrypt

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from luvio_api.models import UserAccount
from luvio_api.serializers import JwtTokenSerializer


class JwtTokenView(TokenObtainPairView):
    serializer_class = JwtTokenSerializer

    def post(self, request: Request):
        primary_email = request.data.get('primary_email', None)
        password = request.data.get('password', None)

        account = UserAccount.objects.get(primary_email=primary_email)
        hashed_pwd = account.password_hashed.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
            print("Password matches!")
            jwt_token = JwtTokenSerializer(
                data=request.data).get_token(account)
            parse_token = {
                'refresh': str(jwt_token),
                'access': str(jwt_token.access_token),
            }
            return Response(status=200, data=parse_token)
        raise exceptions.NotFound(
            {"message": "User with this email or password not found"})
