from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import ProfileType, UserAccount, UserProfile
from luvio_api.serializers import UserProfileSerializer


class UserProfileListView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get existing profiles of the logged in account
        """
        current_user = request.user
        profiles = get_list_or_404(UserProfile, account=current_user)
        return Response(
            [
                {
                    "id": profile.id,
                    "avatar_link": profile.avatar_link,
                    "profile_pitch": profile.profile_pitch,
                    "profile_url": profile.profile_url,
                    "date_created": profile.date_created,
                    "profile_type": profile.profile_type.profile_type,
                }
                for profile in profiles
            ]
        )

    def post(self, request: Request) -> Response:
        """
        Create a new profile for the logged in account
        """
        current_user = request.user
        if UserProfile.objects.filter(
            profile_type=request.data.get("profile_type"), account=current_user
        ).exists():
            return Response(
                {
                    "message": "This account already has a profile with this profile type"
                },
                status=status.HTTP_409_CONFLICT,
            )
        data = {
            "avatar_link": request.data.get("avatar_link", None),
            "profile_pitch": request.data.get("profile_pitch", None),
            "profile_type": request.data.get("profile_type"),
            "profile_url": request.data.get("profile_url", None),
            "account": current_user.id,
        }

        serializer = UserProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(
            {
                "message": "Successfully created profile!",
                "profile_url": profile.profile_url,
                "profile_id": profile.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def _generate_profile_url(self):
        pass
        # TODO: implement url generation (unique for each profile)

    def _get_profile_type_name(self, id: int) -> str:
        return get_object_or_404(ProfileType, pk=id).profile_type


class UserProfileDetailView(APIView):
    def get(self, request: Request, id: int) -> Response:
        """
        Get existing profile of the logged in account based on profile id
        """
        profile = self._get_profile(id, request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request: Request, id: int) -> Response:
        """
        Update an existing profile
        """
        profile = self._get_profile(id, request.user)
        profile.avatar_link = request.data.get("avatar_link", profile.avatar_link)
        profile.profile_pitch = request.data.get("profile_pitch", profile.profile_pitch)
        profile.save()
        return Response(
            {
                "message": "Successfully updated profile!",
            }
        )

    def delete(self, request: Request, id: int) -> Response:
        """
        Delete an existing profile
        """
        self._get_profile(id, request.user).delete()
        return Response(
            {
                "message": "Successfully deleted profile!",
            }
        )

    def _get_profile(self, id: int, account: UserAccount) -> UserProfile:
        return get_object_or_404(UserProfile, pk=id, account=account)
