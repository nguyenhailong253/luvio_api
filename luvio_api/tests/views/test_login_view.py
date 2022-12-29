import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.models import UserAccount


class LoginViewTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        # Ref: https://stackoverflow.com/a/33294746/8749888
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

    def setUp(self):
        self.client = APIClient()

    def test_login_with_username(self):
        """
        Test successfully log in with username
        """
        response = self.client.post(
            "/login/",
            {
                "username": "default_user",
                "password": "default_pw",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "default_user")
        self.assertEqual(response.data["email"], "default@default.com")
        self.assertTrue(response.data["token"])
        self.assertTrue(response.data["user_id"])

    def test_login_with_email(self):
        """
        Test successfully log in with email
        """
        response = self.client.post(
            "/login/",
            {
                "email": "default@default.com",
                "password": "default_pw",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "default_user")
        self.assertEqual(response.data["email"], "default@default.com")
        self.assertTrue(response.data["token"])
        self.assertTrue(response.data["user_id"])

    def test_login_fail(self):
        """
        Test login fails when user not found
        """
        response = self.client.post(
            "/login/",
            {
                "email": "default@default.com",
                "password": "wrong_pwd",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
