import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import (
    Address,
    ProfileType,
    StateAndTerritory,
    Suburb,
    TenantProfilesAddresses,
    UserAccount,
    UserProfile,
)


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
        cls.tenant_profile_type = ProfileType.objects.create(profile_type="tenant")

        # Create a tenant profile
        cls.tenant_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known tenant",
            profile_type=cls.tenant_profile_type,
            profile_url="",
            account=cls.default_user,
        )

        # Create address
        cls.state = StateAndTerritory.objects.create(
            state_code="VIC", name="Victoria", country="Australia"
        )
        cls.suburb = Suburb.objects.create(
            state_and_territory=cls.state, name="New Suburb", postcode="1100"
        )
        Address.objects.create(
            display_address="2/345 Mary Road, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number="2",
            street_number="345",
            street_name="Mary",
            street_type="Road",
            street_type_abbrev="Rd",
        )
        cls.address = Address.objects.create(
            display_address="789 Brian Boulevard, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number=None,
            street_number="789",
            street_name="Brian",
            street_type="Boulevard",
            street_type_abbrev="Bvd",
        )

        # Create address already linked to profile
        TenantProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address,
            move_in_date="2022-12-31",
            move_out_date=None,
            is_current_residence=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_link_address_to_profile(self):
        """
        Test
        """
        response = self.client.post(
            f"/profiles/{self.tenant_profile.id}/addresses/",
            {
                "address": "1/123 John Street, Fake Suburb VIC 1000",
                "unitNumber": "1",
                "streetNumber": "123",
                "streetName": "John",
                "streetTypeLong": "Street",
                "streetType": "St",
                "suburb": "Fake Suburb",
                "postCode": "1000",
                "state": "VIC",
                "moveInDate": "2023-01-01",
                "moveOutDate": "2024-01-01",
                "isCurrentResidence": False,
            },
        ).render()

        address = Address.objects.get(
            display_address="1/123 John Street, Fake Suburb VIC 1000"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TenantProfilesAddresses.objects.filter(
                profile=self.tenant_profile.id, address=address
            ).exists()
        )

    def test_link_address_to_profile_when_move_out_date_is_none(self):
        """
        Test
        """
        response = self.client.post(
            f"/profiles/{self.tenant_profile.id}/addresses/",
            {
                "address": "2/345 Mary Road, New Suburb VIC 1100",
                "unitNumber": "2",
                "streetNumber": "345",
                "streetName": "Mary",
                "streetTypeLong": "Road",
                "streetType": "Rd",
                "suburb": "New Suburb",
                "postCode": "1100",
                "state": "VIC",
                "moveInDate": "2022-12-31",
                "moveOutDate": None,
                "isCurrentResidence": True,
            },
        ).render()

        address = Address.objects.get(
            display_address="2/345 Mary Road, New Suburb VIC 1100"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TenantProfilesAddresses.objects.filter(
                profile=self.tenant_profile.id, address=address
            ).exists()
        )

    def test_link_address_to_profile_when_same_address_and_move_in_date(self):
        """
        Test
        """
        response = self.client.post(
            f"/profiles/{self.tenant_profile.id}/addresses/",
            {
                "address": "789 Brian Boulevard, New Suburb VIC 1100",
                "unitNumber": None,
                "streetNumber": "789",
                "streetName": "Brian",
                "streetTypeLong": "Boulevard",
                "streetType": "Bvd",
                "suburb": "New Suburb",
                "postCode": "1100",
                "state": "VIC",
                "moveInDate": "2022-12-31",
                "moveOutDate": None,
                "isCurrentResidence": True,
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


if __name__ == "__main__":
    unittest.main()
