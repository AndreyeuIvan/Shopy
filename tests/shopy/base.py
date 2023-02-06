from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy

from tests.my_auth.factories import UserFactory
from tests.shopy.factories import ProductFactory, ShopFactory, ReservedFactory, AccountFactory

class BaseUserTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.password = UserFactory().password
        cls.user.set_password(cls.password)
        cls.user.save(update_fields=("password",))
        cls.other_user = UserFactory()
        # cls.password = UserFactory().password
        cls.other_user.set_password(cls.password)
        cls.other_user.save(update_fields=("password",))
        cls.search_url = reverse_lazy("search")
        cls.annulment_url = reverse_lazy("annulment")
        cls.basket_url = "/api/basket/"
        cls.shop = ShopFactory()
        cls.product = ProductFactory(
            name="Milk", shop_name=cls.shop, number_of_units=15
        )
        cls.reserve = ReservedFactory(user=cls.user)
        cls.account = AccountFactory(user=cls.user)
