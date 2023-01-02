import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.common.constants import DATE_FORMAT, PROFILE_TYPES
from luvio_api.models import (
    Address,
    ProfilesAddresses,
    ProfileType,
    StateAndTerritory,
    Suburb,
    UserAccount,
    UserProfile,
)


class ProfilesAddressesTestCase(TestCase):
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
        cls.landlord_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["landlord"]
        )
        cls.agent_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["agent"]
        )
        cls.tenant_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["tenant"]
        )

        # Create profiles
        cls.landlord_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known landlord",
            profile_type=cls.landlord_profile_type,
            profile_url="landlord.com/profile",
            account=cls.default_user,
        )
        cls.agent_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known agent",
            profile_type=cls.agent_profile_type,
            profile_url="agent.com/profile",
            account=cls.default_user,
        )
        cls.tenant_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known tenant",
            profile_type=cls.tenant_profile_type,
            profile_url="tenant.com/profile",
            account=cls.default_user,
        )

        # Create address
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
            display_address="911 Emergency Lane, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number=None,
            street_number="911",
            street_name="Emergency",
            street_type="Lane",
            street_type_abbrev="Ln",
        )
        cls.address3 = Address.objects.create(
            display_address="2/345 Mary Road, New Suburb VIC 1100",
            suburb=cls.suburb,
            unit_number="2",
            street_number="345",
            street_name="Mary",
            street_type="Road",
            street_type_abbrev="Rd",
        )

        # Create addresses already linked to profile
        cls.profile_address_entry1 = ProfilesAddresses.objects.create(
            profile=cls.landlord_profile,
            address=cls.address1,
            profile_type=cls.landlord_profile_type,
            ownership_start_date="2016-01-01",
            ownership_end_date="2018-01-01",
        )
        ProfilesAddresses.objects.create(
            profile=cls.landlord_profile,
            address=cls.address3,
            profile_type=cls.landlord_profile_type,
            ownership_start_date="2010-01-01",
            ownership_end_date="2030-01-01",
            is_current_residence=True,
        )
        cls.profile_address_entry2 = ProfilesAddresses.objects.create(
            profile=cls.agent_profile,
            address=cls.address1,
            profile_type=cls.agent_profile_type,
            management_start_date="2025-01-01",
            management_end_date="2026-01-01",
        )
        ProfilesAddresses.objects.create(
            profile=cls.agent_profile,
            address=cls.address3,
            profile_type=cls.agent_profile_type,
            management_start_date="2010-01-01",
            management_end_date="2030-01-01",
        )
        cls.profile_address_entry3 = ProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address1,
            profile_type=cls.tenant_profile_type,
            move_in_date="2022-01-01",
            is_current_residence=True,
        )
        ProfilesAddresses.objects.create(
            profile=cls.tenant_profile,
            address=cls.address3,
            profile_type=cls.tenant_profile_type,
            move_in_date="2010-01-01",
            move_out_date="2030-01-01",
            is_current_residence=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_link_address_to_landlord_profile(self):
        """
        Test successfully link an address to a landord profile
        """
        response = self.client.post(
            f"/profiles/{self.landlord_profile.id}/addresses/",
            {
                "display_address": "1/123 John Street, Fake Suburb VIC 1000",
                "unit_number": "1",
                "street_number": "123",
                "street_name": "John",
                "street_type": "Street",
                "street_type_abbrev": "St",
                "suburb": "Fake Suburb",
                "postcode": "1000",
                "state": "VIC",
                "move_in_date": None,
                "move_out_date": None,
                "management_start_date": None,
                "management_end_date": None,
                "ownership_start_date": "2023-01-01",
                "ownership_end_date": "2024-01-01",
                "is_current_residence": False,
            },
        ).render()

        address = Address.objects.get(
            display_address="1/123 John Street, Fake Suburb VIC 1000"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["profile_address_id"])
        self.assertTrue(
            ProfilesAddresses.objects.filter(
                profile=self.landlord_profile,
                address=address,
                profile_type=self.landlord_profile_type,
            ).exists()
        )
        self.assertEqual(len(self.landlord_profile.addresses.all()), 3)

    def test_link_address_to_agent_profile(self):
        """
        Test successfully link an address to an agent profile
        """
        response = self.client.post(
            f"/profiles/{self.agent_profile.id}/addresses/",
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
                "management_start_date": "2023-01-01",
                "management_end_date": "2024-01-01",
            },
        ).render()

        address = Address.objects.get(
            display_address="2/345 Mary Road, New Suburb VIC 1100"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["profile_address_id"])
        self.assertTrue(
            ProfilesAddresses.objects.filter(
                profile=self.agent_profile,
                address=address,
                profile_type=self.agent_profile_type,
            ).exists()
        )
        self.assertEqual(len(self.agent_profile.addresses.all()), 3)

    def test_link_address_to_tenant_profile(self):
        """
        Test successfully link an address to a tenant profile
        """
        response = self.client.post(
            f"/profiles/{self.tenant_profile.id}/addresses/",
            {
                "display_address": "1/123 John Street, Fake Suburb VIC 1000",
                "unit_number": "1",
                "street_number": "123",
                "street_name": "John",
                "street_type": "Street",
                "street_type_abbrev": "St",
                "suburb": "Fake Suburb",
                "postcode": "1000",
                "state": "VIC",
                "move_in_date": "2022-01-01",
                "move_out_date": "2023-01-01",
                "is_current_residence": True,
            },
        ).render()

        address = Address.objects.get(
            display_address="1/123 John Street, Fake Suburb VIC 1000"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["profile_address_id"])
        self.assertTrue(
            ProfilesAddresses.objects.filter(
                profile=self.tenant_profile,
                address=address,
                profile_type=self.tenant_profile_type,
            ).exists()
        )
        self.assertEqual(len(self.tenant_profile.addresses.all()), 3)

    def test_link_address_to_landlord_profile_when_same_address_and_ownership_start_date(
        self,
    ):
        """
        Test unable to link an address to current profile if same address and ownership_start_date with other entries
        """
        response = self.client.post(
            f"/profiles/{self.landlord_profile.id}/addresses/",
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
                "ownership_start_date": "2016-01-01",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_link_address_to_agent_profile_when_same_address_and_management_start_date(
        self,
    ):
        """
        Test unable to link an address to current profile if same address and management_start_date with other entries
        """
        response = self.client.post(
            f"/profiles/{self.agent_profile.id}/addresses/",
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
                "management_start_date": "2025-01-01",
                "management_end_date": None,
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_link_address_to_tenant_profile_when_same_address_and_move_in_date(self):
        """
        Test unable to link an address to current profile if same address and move_in_date with other entries
        """
        response = self.client.post(
            f"/profiles/{self.tenant_profile.id}/addresses/",
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
                "move_in_date": "2022-01-01",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_address_in_landlord_profile(self):
        """
        Test successfully update address in a landlord profile
        """
        response = self.client.put(
            f"/profiles/{self.landlord_profile.id}/addresses/{self.profile_address_entry1.id}/",
            {
                "display_address": "911 Emergency Lane, New Suburb VIC 1100",
                "unit_number": None,
                "street_number": "911",
                "street_name": "Emergency",
                "street_type": "Lane",
                "street_type_abbrev": "Ln",
                "suburb": "New Suburb",
                "postcode": "1100",
                "state": "VIC",
                "ownership_start_date": "2022-12-31",
                "ownership_end_date": "2023-12-31",
                "is_current_residence": True,
            },
        ).render()

        profile_address = ProfilesAddresses.objects.get(
            pk=self.profile_address_entry1.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile_address.ownership_start_date.strftime(DATE_FORMAT),
            "2022-12-31",
        )
        self.assertEqual(
            profile_address.ownership_end_date.strftime(DATE_FORMAT),
            "2023-12-31",
        )
        self.assertEqual(profile_address.address, self.address2)
        self.assertTrue(profile_address.is_current_residence)

    def test_update_address_in_agent_profile(self):
        """
        Test successfully update address in an agent profile
        """
        response = self.client.put(
            f"/profiles/{self.agent_profile.id}/addresses/{self.profile_address_entry2.id}/",
            {
                "display_address": "911 Emergency Lane, New Suburb VIC 1100",
                "unit_number": None,
                "street_number": "911",
                "street_name": "Emergency",
                "street_type": "Lane",
                "street_type_abbrev": "Ln",
                "suburb": "New Suburb",
                "postcode": "1100",
                "state": "VIC",
                "management_start_date": "2022-12-31",
                "management_end_date": "2023-12-31",
            },
        ).render()

        profile_address = ProfilesAddresses.objects.get(
            pk=self.profile_address_entry2.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile_address.management_start_date.strftime(DATE_FORMAT),
            "2022-12-31",
        )
        self.assertEqual(
            profile_address.management_end_date.strftime(DATE_FORMAT),
            "2023-12-31",
        )
        self.assertEqual(profile_address.address, self.address2)
        self.assertFalse(profile_address.is_current_residence)

    def test_update_address_in_tenant_profile(self):
        """
        Test successfully update address in a tenant profile
        """
        response = self.client.put(
            f"/profiles/{self.tenant_profile.id}/addresses/{self.profile_address_entry3.id}/",
            {
                "display_address": "911 Emergency Lane, New Suburb VIC 1100",
                "unit_number": None,
                "street_number": "911",
                "street_name": "Emergency",
                "street_type": "Lane",
                "street_type_abbrev": "Ln",
                "suburb": "New Suburb",
                "postcode": "1100",
                "state": "VIC",
                "move_in_date": "2022-12-31",
            },
        ).render()

        profile_address = ProfilesAddresses.objects.get(
            pk=self.profile_address_entry3.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile_address.move_in_date.strftime(DATE_FORMAT),
            "2022-12-31",
        )
        self.assertEqual(profile_address.move_out_date, None)
        self.assertEqual(profile_address.address, self.address2)
        self.assertFalse(profile_address.is_current_residence)

    def test_update_address_in_landlord_profile_when_same_address_and_ownership_start_date(
        self,
    ):
        """
        Test unable to update address in landlord profile when other entries have the same address and ownership start date
        """
        response = self.client.put(
            f"/profiles/{self.landlord_profile.id}/addresses/{self.profile_address_entry1.id}/",
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
                "ownership_start_date": "2010-01-01",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_address_in_agent_profile_when_same_address_and_management_start_date(
        self,
    ):
        """
        Test unable to update address in agent profile when other entries have the same address and management start date
        """
        response = self.client.put(
            f"/profiles/{self.agent_profile.id}/addresses/{self.profile_address_entry2.id}/",
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
                "management_start_date": "2010-01-01",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_address_in_tenant_profile_when_same_address_and_move_in_date(
        self,
    ):
        """
        Test unable to update address in tenant profile when other entries have the same address and move in date
        """
        response = self.client.put(
            f"/profiles/{self.tenant_profile.id}/addresses/{self.profile_address_entry3.id}/",
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
                "move_in_date": "2010-01-01",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_delete_address_in_profile(self):
        """
        Test delete address in current profile
        """
        response = self.client.delete(
            f"/profiles/{self.landlord_profile.id}/addresses/{self.profile_address_entry1.id}/",
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            ProfilesAddresses.objects.filter(pk=self.profile_address_entry1.id).exists()
        )


if __name__ == "__main__":
    unittest.main()
