# sourcery skip: snake-case-functions
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from tests.my_auth.factories import UserFactory


class BaseUserTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.password = UserFactory().password
        cls.user.set_password(cls.password)
        cls.user.save(update_fields=('password',))
        cls.other_user = UserFactory()
        #cls.password = UserFactory().password
        cls.other_user.set_password(cls.password)
        cls.other_user.save(update_fields=('password',))
        cls.login_url = reverse_lazy('login')
        cls.logout_url = reverse_lazy('logout')
        cls.register_url = reverse_lazy('register')
