# sourcery skip: snake-case-functions
from django.test import TestCase

from tests.my_auth.factories import UserFactory


class TestUserModel(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_phone_field_exists(self) -> None:
        user_fields = [field.name for field in self.user._meta.get_fields()]
        self.assertIn('phone_number', user_fields)

    def test_email_field_exists(self) -> None:
        user_fields = [field.name for field in self.user._meta.get_fields()]
        self.assertIn('email', user_fields)
