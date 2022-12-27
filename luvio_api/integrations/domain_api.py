from typing import Any, Iterable

import environ
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

env = environ.Env()
# reading .env file - not checked into git
environ.Env.read_env()

DOMAIN_API_AUTH_URL = "https://auth.domain.com.au/v1/connect/token"

DOMAIN_API_PROPERTIES_URL = "https://api.domain.com.au/v1/properties"

TIMEOUT = 30


class DomainApiClient:
    def __init__(self):
        # When calling Domain API, if receive 401, meaning token might have expired, try refresh token and then re call
        self.access_token = self._get_access_token()

    def _get_access_token(self) -> str:
        try:
            return env("DOMAIN_API_TOKEN")
        except Exception:
            return self._refresh_token()

    def _refresh_token(self) -> str:
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
        return response.json()["access_token"]

    def _get(self, url: str) -> Iterable[Any]:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                self._refresh_token()
                headers = {"Authorization": f"Bearer {self.access_token}"}
                response = requests.get(url, headers=headers, timeout=TIMEOUT)
            else:
                raise e
        return response.json()

    def get_address_suggestions(self, search_term_url_encoded: str) -> Iterable[Any]:
        url = f"{DOMAIN_API_PROPERTIES_URL}/_suggest?terms={search_term_url_encoded}&channel=All"
        return self._get(url)
