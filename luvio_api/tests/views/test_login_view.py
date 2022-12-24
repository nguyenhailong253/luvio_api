import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from luvio_api.views import LoginView
from luvio_api.models import UserAccount


class LoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ref: https://stackoverflow.com/a/33294746/8749888
        default_user = UserAccount.objects.create(
            email="default@default.com",
            username="default_user",
            first_name="default_fn",
            last_name="default_ln",
            date_of_birth="2022-01-01",
            is_active=True,
        )
        default_user.set_password("default_pw")
        default_user.save()
        cls.factory = APIRequestFactory()
        cls.view = LoginView.as_view()

    def test_login_with_username(self):
        """
        Test successfully log in with username
        """
        request = self.factory.post(
            "/login/",
            {
                "username": "default_user",
                "password": "default_pw",
            },
        )
        response = self.view(request)
        response.render()
        resp_body = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_body["username"], "default_user")
        self.assertEqual(resp_body["email"], "default@default.com")
        self.assertTrue(resp_body["token"])
        self.assertTrue(resp_body["user_id"])

    def test_login_with_email(self):
        """
        Test successfully log in with email
        """
        request = self.factory.post(
            "/login/",
            {
                "email": "default@default.com",
                "password": "default_pw",
            },
        )
        response = self.view(request)
        response.render()
        resp_body = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_body["username"], "default_user")
        self.assertEqual(resp_body["email"], "default@default.com")
        self.assertTrue(resp_body["token"])
        self.assertTrue(resp_body["user_id"])

    def test_login_fail(self):
        """
        Test login fails when user not found
        """
        request = self.factory.post(
            "/login/",
            {
                "email": "default@default.com",
                "password": "wrong_pwd",
            },
        )
        response = self.view(request)
        response.render()
        resp_body = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
