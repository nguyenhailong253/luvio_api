import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from luvio_api.common.constants import DATE_FORMAT
from luvio_api.models import UserAccount


class UserAccountTestCase(TestCase):
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

        # Another user
        UserAccount.objects.create(
            email="another_default@default.com",
            username="another_default_user",
            password="default_pwd",
            first_name="default_fn",
            last_name="default_ln",
            date_of_birth="2022-01-01",
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

    def test_update_user(self):
        """
        Test update existing user
        """
        response = self.client.put(
            "/accounts/",
            {
                "email": "default@default.com",
                "username": "default_user_updated",
                "first_name": "default_fn_updated",
                "last_name": "default_ln_updated",
                "date_of_birth": "2022-01-02",
                "mobile": "0412345678",
            },
        ).render()

        updated_user = UserAccount.objects.get(email="default@default.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.username, "default_user_updated")
        self.assertEqual(updated_user.first_name, "default_fn_updated")
        self.assertEqual(updated_user.last_name, "default_ln_updated")
        self.assertEqual(updated_user.date_of_birth.strftime(DATE_FORMAT), "2022-01-02")
        self.assertEqual(updated_user.mobile, "0412345678")

    def test_update_user_non_unique_username(self):
        """
        Test update user with username same with other user
        """
        response = self.client.put(
            "/accounts/",
            {
                "username": "another_default_user",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_non_unique_email(self):
        """
        Test update user with email same with other user
        """
        response = self.client.put(
            "/accounts/",
            {
                "email": "another_default@default.com",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        """
        Test change user password
        """
        response = self.client.put(
            "/accounts/password/",
            {
                "old_password": "default_pw",
                "new_password": "new_pw",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password_with_incorrect_old_password(self):
        """
        Test change user password
        """
        response = self.client.put(
            "/accounts/password/",
            {
                "old_password": "wrong pwd",
                "new_password": "new_pw",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_no_new_password(self):
        """
        Test change user password
        """
        response = self.client.put(
            "/accounts/password/",
            {
                "old_password": "default_pw",
                "new_password": "",
            },
        ).render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()
