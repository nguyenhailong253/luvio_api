import unittest

from django.test import TestCase
from rest_framework import exceptions

from luvio_api.common.check_profile_type import check_profile_type
from luvio_api.common.constants import PROFILE_TYPES
from luvio_api.models import ProfileType, UserAccount, UserProfile


class CheckProfileTypeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
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

        # Set up profile type
        cls.agent_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["agent"]
        )
        cls.tenant_profile_type = ProfileType.objects.create(
            profile_type=PROFILE_TYPES["tenant"]
        )

        # Create an agent profile
        cls.agent_profile = UserProfile.objects.create(
            avatar_link="https://img.com",
            profile_pitch="Hi I'm a well known agent",
            profile_type=cls.agent_profile_type,
            profile_url="",
            account=cls.default_user,
        )

    def test_check_profile_type_should_not_raise_exception(self):
        """
        Test profile is the correct type - should not raise any exceptions
        """
        check_profile_type(self.agent_profile.id, PROFILE_TYPES["agent"])

    def test_check_profile_type_should_raise_exception(self):
        """
        Test profile is NOT the correct type - should raise validation exception
        """
        with self.assertRaises(exceptions.ValidationError):
            check_profile_type(self.agent_profile.id, PROFILE_TYPES["tenant"])


if __name__ == "__main__":
    unittest.main()
