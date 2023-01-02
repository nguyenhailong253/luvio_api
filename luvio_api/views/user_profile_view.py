import logging

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.common.constants import DEFAULT_LOGGER
from luvio_api.models import UserAccount, UserProfile
from luvio_api.serializers import (
    UserProfileCreateOrUpdateSerializer,
    UserProfileGetFullDetailSerializer,
    UserProfileListSerializer,
)

logger = logging.getLogger(DEFAULT_LOGGER)


class UserProfileListView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get existing profiles of the logged in account
        """
        current_user = request.user
        profiles = get_list_or_404(UserProfile, account=current_user)
        serializer = UserProfileListSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new profile for the logged in account
        """
        current_user = request.user
        if UserProfile.objects.filter(
            profile_type=request.data.get("profile_type"), account=current_user
        ).exists():
            logger.error(
                f"Failed to create a new profile because this profile type already exists in this account. User '{current_user}'"
            )
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

        serializer = UserProfileCreateOrUpdateSerializer(data=data)
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


class UserProfileDetailView(APIView):
    def get(self, request: Request, profile_id: int) -> Response:
        """
        Get existing profile of the logged in account based on profile id
        """
        profile = self._get_profile(profile_id, request.user)
        serializer = UserProfileGetFullDetailSerializer(profile)
        return Response(serializer.data)

    def put(self, request: Request, profile_id: int) -> Response:
        """
        Update an existing profile
        """
        profile = self._get_profile(profile_id, request.user)
        serializer = UserProfileCreateOrUpdateSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Successfully updated profile!",
            }
        )

    def delete(self, request: Request, profile_id: int) -> Response:
        """
        Delete an existing profile
        """
        self._get_profile(profile_id, request.user).delete()
        return Response(
            {
                "message": "Successfully deleted profile!",
            }
        )

    def _get_profile(self, profile_id: int, account: UserAccount) -> UserProfile:
        return get_object_or_404(UserProfile, pk=profile_id, account=account)
