import unittest
from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import StateAndTerritory, UserAccount


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

        # Create state
        cls.vic_state = StateAndTerritory.objects.create(
            state_code="VIC", name="Victoria", country="Australia"
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_get_address_suggestions_when_query_param_not_provided(self):
        """
        Test get address suggestions when query param "term" has no value
        """
        response = self.client.get("/addresses/suggestions/?term=").render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "luvio_api.views.address_view.DomainApiClient.get_address_suggestions",
        MagicMock(
            return_value=[
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
        ),
    )
    def test_get_address_suggestions(self):
        """
        Test get address suggestions when query param "term" is provided
        """
        response = self.client.get(
            "/addresses/suggestions/?term=1/123%20john%20street"
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


if __name__ == "__main__":
    unittest.main()
