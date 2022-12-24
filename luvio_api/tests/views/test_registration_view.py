import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from luvio_api.views import RegistrationView
from luvio_api.models import UserAccount


class RegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserAccount.objects.create(
            email="default@default.com",
            username="default_user",
            password="default_pw",
            first_name="default_fn",
            last_name="default_ln",
            date_of_birth="2022-01-01",
            is_active=True,
        )
        cls.factory = APIRequestFactory()
        cls.view = RegistrationView.as_view()

    def test_register_account(self):
        """
        Test successfully register an account
        """
        request = self.factory.post(
            "/registration/",
            {
                "email": "test@test.com",
                "username": "test",
                "first_name": "wow",
                "last_name": "woah",
                "password": "secret",
                "date_of_birth": "01/01/2022",
                "is_active": True,
            },
        )
        response = self.view(request)
        response.render()
        resp_body = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_body["username"], "test")
        self.assertEqual(resp_body["email"], "test@test.com")
        self.assertTrue(resp_body["token"])
        self.assertTrue(resp_body["user_id"])

    def test_register_account_already_existed(self):
        """
        Test registration when account email or username already exist
        """
        request = self.factory.post(
            "/registration/",
            {
                "email": "default@default.com",
                "username": "default_user",
                "first_name": "wow",
                "last_name": "woah",
                "password": "secret",
                "date_of_birth": "01/01/2022",
                "is_active": True,
            },
        )
        response = self.view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()
