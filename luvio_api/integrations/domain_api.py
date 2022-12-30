from typing import Any, Iterable

import environ
import requests
from django.core.exceptions import ImproperlyConfigured
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

from luvio_api.common.domain_api_utils import (
    convert_address_suggestion_fields_to_snake_case,
)

env = environ.Env()
# reading .env file - not checked into git
environ.Env.read_env()

DOMAIN_API_AUTH_URL = "https://auth.domain.com.au/v1/connect/token"

DOMAIN_API_PROPERTIES_URL = "https://api.domain.com.au/v1/properties"

TIMEOUT = 30


class DomainApiClient:
    def __init__(self):
        # When calling Domain API, if receive 401, meaning token might have expired, try refresh token and then re call
        self.access_token = None
        self._set_access_token()

    def _set_access_token(self):
        try:
            self.access_token = env("DOMAIN_API_TOKEN")
        except ImproperlyConfigured as e:
            print(f"No API token found for Domain API: {e}")
            self._refresh_token()

    def _refresh_token(self):
        client_id = env("DOMAIN_API_CLIENT_ID")
        client_secrets = env("DOMAIN_API_CLIENT_SECRET")
        req_body = {
            "scope": env("DOMAIN_API_SCOPE"),
            "grant_type": "client_credentials",
        }

        response = requests.post(
            DOMAIN_API_AUTH_URL,
            data=req_body,
            auth=HTTPBasicAuth(client_id, client_secrets),
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]

    def _get(self, url: str) -> Iterable[Any]:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _make_get_request(self, url: str):
        try:
            return self._get(url)
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                self._refresh_token()
                return self._get(url)
            else:
                raise e

    def get_address_suggestions(self, search_term_url_encoded: str) -> Iterable[Any]:
        url = f"{DOMAIN_API_PROPERTIES_URL}/_suggest?terms={search_term_url_encoded}&channel=All"
        return convert_address_suggestion_fields_to_snake_case(
            self._make_get_request(url)
        )
