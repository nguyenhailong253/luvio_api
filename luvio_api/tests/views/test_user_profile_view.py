import unittest
from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import ProfileType, UserAccount, UserProfile


class UserProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Main default user for testing
        cls.default_user = UserAccount.objects.create(
            email="default@default.com",
            username="default_user",
            first_name="default_fn",
            last_name="default_ln",
            date_of_birth="2022-01-01",
            is_active=True,
        )
        cls.default_user.set_password("default_pw")
        cls.default_user.save()

        # Set up profile types
        cls.agent_profile_type = ProfileType.objects.create(profile_type="agent")
        cls.landlord_profile_type = ProfileType.objects.create(profile_type="landlord")
        cls.tenant_profile_type = ProfileType.objects.create(profile_type="tenant")

        # Create an agent profile
        cls.agent_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known agent",
            profile_type=cls.agent_profile_type,
            profile_url="agenturl",
            account=cls.default_user,
        )

        # Create a tenant profile
        cls.tenant_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known tenant",
            profile_type=cls.tenant_profile_type,
            profile_url="tenanturl",
            account=cls.default_user,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_get_profile(self):
        """
        Test get all existing profiles
        """
        response = self.client.get("/profiles/").render()
        expected_response = [
            {
                "id": self.agent_profile.id,
                "avatar_link": "https://img.com",
                "profile_pitch": "Hi I'm a well known agent",
                "profile_url": "agenturl",
                "date_created": datetime.strptime(
                    self.agent_profile.date_created, "%Y-%m-%d"
                ).date(),
                "profile_type": "agent",
            },
            {
                "id": self.tenant_profile.id,
                "avatar_link": "https://img.com",
                "profile_pitch": "Hi I'm a well known tenant",
                "profile_url": "tenanturl",
                "date_created": datetime.strptime(
                    self.tenant_profile.date_created, "%Y-%m-%d"
                ).date(),
                "profile_type": "tenant",
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_create_profile(self):
        """
        Test create a profile
        """
        response = self.client.post(
            "/profiles/",
            {
                "avatar_link": "img.com",
                "profile_pitch": "This is a tenant profile",
                "profile_type": self.landlord_profile_type.id,
                "profile_url": "url",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["profile_id"])

    def test_create_already_exist_profile(self):
        """
        Test create a profile which already exists
        """
        response = self.client.post(
            "/profiles/",
            {
                "avatar_link": "https://img.com",
                "profile_pitch": "This is a duplicated profile",
                "profile_type": self.agent_profile_type.id,
                "profile_url": "testurl",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_profile(self):
        """
        Test update existing profile
        """
        response = self.client.put(
            f"/profiles/{self.tenant_profile.id}/",
            {
                "avatar_link": "https://new_avatar.com",
                "profile_pitch": "An update on my tenant profile",
            },
        ).render()

        updated_profile = UserProfile.objects.get(
            profile_type=self.tenant_profile_type.id, account=self.default_user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_profile.avatar_link, "https://new_avatar.com")
        self.assertEqual(
            updated_profile.profile_pitch, "An update on my tenant profile"
        )

    def test_delete_profile(self):
        """
        Test delete existing profile
        """
        response = self.client.delete(
            f"/profiles/{self.tenant_profile.id}/",
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(
                UserProfile.objects.filter(
                    profile_type=self.tenant_profile_type.id, account=self.default_user
                )
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
