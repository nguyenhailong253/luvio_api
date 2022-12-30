import unittest

from django.test import TestCase

from luvio_api.common.domain_api_utils import (
    convert_address_suggestion_fields_to_snake_case,
    store_suburb_and_address_data,
)
from luvio_api.models import Address, StateAndTerritory, Suburb


class DomainApiUtilsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create state
        cls.vic_state = StateAndTerritory.objects.create(
            state_code="VIC", name="Victoria", country="Australia"
        )

        # Create fake suburb
        cls.fake_suburb = Suburb.objects.create(
            state_and_territory=cls.vic_state,
            name="Fake Suburb",
            postcode="1000",
        )

        # Create fake address
        cls.fake_address = Address.objects.create(
            suburb=cls.fake_suburb,
            display_address="1/123 John Street, Fake Suburb VIC 1000",
            unit_number="1",
            street_number="123",
            street_name="John",
            street_type="Street",
            street_type_abbrev="St",
        )

    def test_store_suburb_and_address_data_where_data_already_exist(self):
        """
        Test store data from domain API in which the data already exist
        i.e Address and suburb already exist in our DB
        """
        addresses = [
            {
                "display_address": "1/123 John Street, Fake Suburb VIC 1000",
                "unit_number": "1",
                "street_number": "123",
                "street_name": "John",
                "street_type_abbrev": "St",
                "street_type": "Street",
                "suburb": "Fake Suburb",
                "postcode": "1000",
                "state": "VIC",
            },
        ]
        store_suburb_and_address_data(addresses)

        self.assertTrue(
            Address.objects.filter(
                display_address="1/123 John Street, Fake Suburb VIC 1000"
            ).exists()
        )
        self.assertTrue(Suburb.objects.filter(name="Fake Suburb").exists())

    def test_store_suburb_and_address_data_where_data_not_exist(self):
        """
        Test store data from domain API in which the data do not exist
        i.e Address and suburb do not exist in our DB
        """
        addresses = [
            {
                "display_address": "900/456 Mary Road, New Suburb VIC 1100",
                "unit_number": "900",
                "street_number": "456",
                "street_name": "Mary",
                "street_type_abbrev": "Rd",
                "street_type": "Road",
                "suburb": "New Suburb",
                "postcode": "1100",
                "state": "VIC",
            },
        ]
        store_suburb_and_address_data(addresses)

        self.assertEqual(len(Address.objects.all()), 2)
        self.assertEqual(len(Suburb.objects.all()), 2)
        self.assertTrue(
            Address.objects.filter(
                display_address="900/456 Mary Road, New Suburb VIC 1100"
            ).exists()
        )
        self.assertTrue(Suburb.objects.filter(name="New Suburb").exists())

    def test_convert_address_suggestion_fields_to_snake_case(self):
        """
        Convert Domain API's address suggestion's response body to snake case
        """
        fake_response = [
            {
                "address": "1/123 John Street, Fake Suburb VIC 1000",
                "addressComponents": {
                    "unitNumber": "1",
                    "streetNumber": "123",
                    "streetName": "John",
                    "streetType": "St",
                    "streetTypeLong": "Street",
                    "suburb": "Fake Suburb",
                    "postCode": "1000",
                    "state": "VIC",
                },
                "id": "NC-6907-CZ",
                "relativeScore": 100,
            }
        ]

        expected = [
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
            }
        ]

        actual = convert_address_suggestion_fields_to_snake_case(fake_response)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
