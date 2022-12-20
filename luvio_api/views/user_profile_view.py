from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from luvio_api.models import UserProfile
from luvio_api.serializers import UserProfileSerializer


class UserProfileView(APIView):

    def get(self, request: Request, format=None):
        """
        Get existing profiles of the logged in account
        """
        # Ref: https://stackoverflow.com/a/12615192/8749888
        current_user = request.user

        profiles = UserProfile.objects.filter(account=current_user)
        if len(profiles) == 0:
            raise exceptions.NotFound(
                {'message': 'This account has no profiles'})
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        """
        Create a new profile for the logged in account
        """
        current_user = request.user
        data = {
            'avatar_link': request.data.get('avatar_link', None),
            'profile_pitch': request.data.get('profile_pitch', None),
            'profile_type': request.data.get('profile_type', None),
            'profile_url': 'test.com.au',
            'account': current_user.id
        }

        serializer = UserProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            'message': "Successfully created profile!",
            'profile_url': profile.profile_url,
        })

    def generate_tiny_url(self):
        pass
        # TODO: implement unique, tiny url
