from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from luvio_api.models import (
    UserAccount,
    UserProfile,
    ProfileType,
    TenantProfilesAddresses,
    LandlordProfilesAddresses,
    AgentProfilesAddresses,
    Address,
)
from luvio_api.serializers import (
    UserProfileSerializer,
    AddressSerializer,
    LandlordProfilesAddressesSerializer,
)


class UserProfileListView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get existing profiles of the logged in account
        """
        current_user = request.user
        profiles = get_list_or_404(UserProfile, account=current_user)
        serializer = UserProfileSerializer(profiles, many=True)
        all_profiles = [
            {
                **profile,
                "profile_type_name": self._get_profile_type_name(
                    profile["profile_type"]
                ),
            }
            for profile in serializer.data
        ]
        return Response(all_profiles)

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
        profile_id = profile.id
        profile_type_id = profile.profile_type
        print(f"type id: {profile_type_id}, id: {profile_id}")
        serializer = UserProfileSerializer(profile)
        linked_addresses = get_list_or_404(
            LandlordProfilesAddresses, profile=profile_id
        )
        print(f"length: {len(linked_addresses)}")
        addresses = [
            {
                "ownership_start_date": linked_address["ownership_start_date"],
                "ownership_end_date": linked_address["ownership_end_date"],
                "is_current_residence": linked_address["is_current_residence"],
                **AddressSerializer(
                    Address.objects.get(pk=linked_address["address"])
                ).data,
            }
            for linked_address in LandlordProfilesAddressesSerializer(
                linked_addresses, many=True
            ).data
        ]
        return Response({**serializer.data, "addresses": addresses})

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
