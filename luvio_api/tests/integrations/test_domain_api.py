import unittest
from unittest.mock import MagicMock, Mock, patch

from requests.exceptions import HTTPError

from luvio_api.integrations.domain_api import DomainApiClient


# Ref: https://realpython.com/python-mock-library/
class TestDomainApiClient(unittest.TestCase):
    @patch(
        "luvio_api.integrations.domain_api.DomainApiClient._set_access_token",
    )
    @patch(
        "luvio_api.integrations.domain_api.DomainApiClient._refresh_token",
    )
    @patch(
        "luvio_api.integrations.domain_api.DomainApiClient._get",
    )
    def test_get_request_with_invalid_token(
        self, mock_get: Mock, mock_refresh_token: Mock, mock_set_access_token: Mock
    ):
        """
        Test sending GET request to Domain API
        """
        client = DomainApiClient()
        failed_response_mock = HTTPError()
        failed_response_mock.response = MagicMock()
        failed_response_mock.response.status_code = 401
        failed_response_mock.response.content = {
            "type": "https://developer.domain.com.au/docs/latest/conventions/access",
            "title": "Not Authorized",
            "detail": "Unable to verify credentials",
        }

        success_response_mock = [
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

        mock_get.side_effect = [failed_response_mock, success_response_mock]

        result = client.get_address_suggestions("1/123%20john%20street")

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
