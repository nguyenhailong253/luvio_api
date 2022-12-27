import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.common.constants import PROFILE_ADDRESS_ID, PROFILE_TYPES
from luvio_api.models import (
    Address,
    ProfileType,
    StateAndTerritory,
    Suburb,
    TenantProfilesAddresses,
    UserAccount,
    UserProfile,
)


class TenantProfilesAddressesTestCase(TestCase):
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
        cls.tenant_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["tenant"]
        )

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
            display_address="911 Emergency Lane, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number=None,
            street_number="911",
            street_name="Emergency",
            street_type="Lane",
            street_type_abbrev="Ln",
        )

        # Create address already linked to profile
        cls.profileAddressEntry1 = TenantProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address1,
            move_in_date="2022-12-31",
            move_out_date=None,
            is_current_residence=True,
        )
        cls.profileAddressEntry2 = TenantProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address2,
            move_in_date="2025-01-01",
            move_out_date="2026-01-01",
            is_current_residence=False,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_link_address_to_profile(self):
        """
        Test successfully link an address to current profile
        """
        response = self.client.post(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
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
        self.assertTrue(response.data[PROFILE_ADDRESS_ID])
        self.assertTrue(
            TenantProfilesAddresses.objects.filter(
                profile=self.tenant_profile.id, address=address
            ).exists()
        )

    def test_link_address_to_profile_when_move_out_date_is_none(self):
        """
        Test successfully link an address to current profile even when move_out_date is none
        """
        response = self.client.post(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
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
        self.assertTrue(response.data[PROFILE_ADDRESS_ID])
        self.assertTrue(
            TenantProfilesAddresses.objects.filter(
                profile=self.tenant_profile.id, address=address
            ).exists()
        )

    def test_link_address_to_profile_when_same_address_and_move_in_date(self):
        """
        Test unable to link an address to current profile if same address and move_in_date with other entries
        """
        response = self.client.post(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
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

    def test_update_address_in_profile(self):
        """
        Test successfully update address in current profile
        """
        response = self.client.put(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
            {
                "profileAddressId": self.profileAddressEntry1.id,
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
                "moveOutDate": "2023-12-31",
                "isCurrentResidence": True,
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            TenantProfilesAddresses.objects.get(
                pk=self.profileAddressEntry1.id
            ).move_out_date.strftime("%Y-%m-%d"),
            "2023-12-31",
        )

    def test_update_address_in_profile_when_same_address_and_move_in_date(self):
        """
        Test unable to update address in current profile when other entries have the same address and move in date
        """
        response = self.client.put(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
            {
                "profileAddressId": self.profileAddressEntry2.id,
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
                "moveOutDate": "2023-12-31",
                "isCurrentResidence": True,
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_delete_address_in_profile(self):
        """
        Test delete address in current profile
        """
        response = self.client.delete(
            f"/profiles/tenant-profiles/{self.tenant_profile.id}/addresses/",
            {
                "profileAddressId": self.profileAddressEntry2.id,
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            TenantProfilesAddresses.objects.filter(
                pk=self.profileAddressEntry2.id
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
