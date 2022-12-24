import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import UserAccount


class RegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_user = UserAccount.objects.create(
            email="default@default.com",
            username="default_user",
            password="default_pw",
            first_name="default_fn",
            last_name="default_ln",
            date_of_birth="2022-01-01",
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_register_account(self):
        """
        Test successfully register an account
        """
        response = self.client.post(
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
        ).render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@test.com")
        self.assertTrue(response.data["token"])
        self.assertTrue(response.data["user_id"])

    def test_register_account_already_existed(self):
        """
        Test registration when account email or username already exist
        """
        response = self.client.post(
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
        ).render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()
