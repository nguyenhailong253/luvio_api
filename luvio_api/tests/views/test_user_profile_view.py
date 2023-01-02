import json
import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import (
    Address,
    ProfilesAddresses,
    ProfileType,
    StateAndTerritory,
    Suburb,
    UserAccount,
    UserProfile,
)


class UserProfileTestCase(TestCase):
    maxDiff = None

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

        # Create addresses linked to a profile
        cls.state = StateAndTerritory.objects.create(
            state_code="VIC", name="Victoria", country="Australia"
        )
        cls.suburb = Suburb.objects.create(
            state_and_territory=cls.state, name="New Suburb", postcode="1100"
        )
        cls.address1 = Address.objects.create(
            display_address="789 Brian Boulevard, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number=None,
            street_number="789",
            street_name="Brian",
            street_type="Boulevard",
            street_type_abbrev="Bvd",
        )
        cls.address2 = Address.objects.create(
            display_address="2/345 Mary Road, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number="2",
            street_number="345",
            street_name="Mary",
            street_type="Road",
            street_type_abbrev="Rd",
        )
        cls.profile_address_entry1 = ProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address1,
            profile_type=cls.tenant_profile_type,
            move_in_date="2022-01-01",
            is_current_residence=True,
        )
        cls.profile_address_entry2 = ProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address2,
            profile_type=cls.tenant_profile_type,
            move_in_date="2010-01-01",
            move_out_date="2030-01-01",
            is_current_residence=False,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_get_profiles(self):
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
                "date_created": self.agent_profile.date_created,
                "profile_type": "agent",
            },
            {
                "id": self.tenant_profile.id,
                "avatar_link": "https://img.com",
                "profile_pitch": "Hi I'm a well known tenant",
                "profile_url": "tenanturl",
                "date_created": self.tenant_profile.date_created,
                "profile_type": "tenant",
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data)), expected_response)

    def test_get_single_profile(self):
        """
        Test get details of 1 profile
        """
        response = self.client.get(f"/profiles/{self.tenant_profile.id}/").render()
        expected_response = {
            "avatar_link": "https://img.com",
            "profile_pitch": "Hi I'm a well known tenant",
            "profile_url": "tenanturl",
            "date_created": self.tenant_profile.date_created,
            "profile_type": "tenant",
            "addresses": [
                {
                    "display_address": "789 Brian Boulevard, New Suburb VIC 1100",
                    "unit_number": None,
                    "street_number": "789",
                    "street_name": "Brian",
                    "street_type": "Boulevard",
                    "street_type_abbrev": "Bvd",
                    "suburb": "New Suburb",
                    "postcode": "1100",
                    "state": "VIC",
                    "move_in_date": self.profile_address_entry1.move_in_date,
                    "move_out_date": None,
                    "management_start_date": None,
                    "management_end_date": None,
                    "ownership_start_date": None,
                    "ownership_end_date": None,
                    "is_current_residence": True,
                    "profile_address_relation_id": self.profile_address_entry1.id,
                },
                {
                    "display_address": "2/345 Mary Road, New Suburb VIC 1100",
                    "unit_number": "2",
                    "street_number": "345",
                    "street_name": "Mary",
                    "street_type": "Road",
                    "street_type_abbrev": "Rd",
                    "suburb": "New Suburb",
                    "postcode": "1100",
                    "state": "VIC",
                    "move_in_date": self.profile_address_entry2.move_in_date,
                    "move_out_date": self.profile_address_entry2.move_out_date,
                    "management_start_date": None,
                    "management_end_date": None,
                    "ownership_start_date": None,
                    "ownership_end_date": None,
                    "is_current_residence": False,
                    "profile_address_relation_id": self.profile_address_entry2.id,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(json.dumps(response.data, default=str)), expected_response
        )

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
