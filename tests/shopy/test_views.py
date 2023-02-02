from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from tests.shopy.factories import ProductFactory
from tests.my_auth.factories import UserFactory
from tests.shopy.base import BaseUserTest
from shopy.serializers import ProductSerializer
from shopy.models import Reserved, Account, Product


class PurchaseListAPIViewTestCase(BaseUserTest):
    def test_with_some_products_created_by_one_user(self):
        products = ProductFactory.create_batch(5)
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        response = self.client.get(self.search_url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        self.assertTrue(products[0].name == response.data[1].get("name"))

    def test_product_search_get_list_of_products(self):
        client = APIClient()
        client.login(username=self.user.username, password=self.password)
        # url_login = reverse('login')
        # res = self.client.post(url_login,{"username":self.user.username, "password":self.password})
        response = client.get(self.search_url)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        # import pdb;pdb.set_trace()

    def test_product_search_get_product_by_using_filter_name_of_the_product(self):
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        filter = "name"
        url_filter = f"{self.search_url}?{filter}={self.product.name}"
        response = self.client.get(url_filter).data
        self.assertTrue(self.product.name == response[0].get("name"))
        # print(response)

    def test_product_search_get_product_by_using_filter_name_of_the_shop(self):
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        products = ProductFactory.create_batch(5)
        filter = "shop_name"
        url_filter = f"{self.search_url}?{filter}={self.product.shop_name}"
        response = self.client.get(url_filter).data
        # import pdb;pdb.set_trace()
        # self.assertTrue(self.product.name == response[0].get('name'))
        # import pdb;pdb.set_trace()

    def test_product_search_get_product_by_using_ordering_by_price_for_unit(self):
        """
        We are login in.
        We create 5 products and one is default, Milk.
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        products = [
            ProductFactory.create(price_for_unit=round(Decimal(n), 2))
            for n in [1.91, 1.84, 2.95, 2.51]
        ]
        order_value = "price_for_unit"
        url_filter = f"{self.search_url}?ordering={order_value}"
        response = self.client.get(url_filter).data
        products.append(self.product)
        # print(response)
        # import pdb;pdb.set_trace()
        sorted_result = sorted(products, key=lambda x: x.price_for_unit)
        self.assertTrue(float(sorted_result[0].price_for_unit)) == float(
            (response[0].get("price_for_unit"))
        )

    def test_product_search_get_product_by_using_ordering_by_price_for_kilo(self):
        """
        We are login in.
        We create 5 products and one is default, Milk.
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        products = []
        for n in [(1.91, 0.4), (1.84, 0.5), (2.95, 0.8), (2.51, 0.9)]:
            products.append(
                ProductFactory.create(price_for_unit=float(n[0]), unit=float(n[1]))
            )
        order_value = "-price_for_kilo"
        url_filter = f"{self.search_url}/?ordering={order_value}"
        response = self.client.get(url_filter).data
        products.append(self.product)
        # print(response)
        # import pdb;pdb.set_trace()
        sorted_result = sorted(products, key=lambda x: x.price_for_kilo, reverse=True)
        # print(sorted_result)
        self.assertTrue(float(sorted_result[0].price_for_kilo)) == float(
            (response[0].get("price_for_kilo"))
        )

    def test_product_search_get_product_by_using_ordering_by_price_for_kilo_and_price_for_unit(
        self,
    ):
        """
        We are login in.
        We create 5 products and one is default, Milk.
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        products = []
        for n in [(1.91, 0.4), (1.84, 0.5), (2.95, 0.8), (2.51, 0.9)]:
            products.append(
                ProductFactory.create(price_for_unit=float(n[0]), unit=float(n[1]))
            )
        order_value = "-price_for_kilo, -price_for_unit"
        url_filter = f"{self.search_url}/?ordering={order_value}"
        response = self.client.get(url_filter).data
        products.append(self.product)

        sorted_result_first_time = sorted(
            products, key=lambda x: x.price_for_kilo, reverse=True
        )
        sorted_result_second_time = sorted(
            sorted_result_first_time, key=lambda x: x.price_for_unit, reverse=True
        )

        self.assertTrue(float(sorted_result_second_time[0].price_for_kilo)) == float(
            (response[0].get("price_for_kilo"))
        )

class AnnulmentGenericAPIViewTestCase(APIClient):

    def test_create_serveral_objects_apply_patch_method_success(self):
        """
        1. Получаем доступ.
        2. Создаем несколько объектов.
        3. Нажимаем Buy(patch)
        4. Проверяем аккаунт
        5. Проверяем количество резерва
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        batch_of_products = ProductFactory.create_batch(5)
        response = self.client.patch(self.annulment_url)

    def test_create_serveral_objects_apply_patch_method_success(self):
        """
        1. Получаем доступ.
        2. Создаем несколько объектов.
        3. Нажимаем Clear(delete)
        4. Проверяем аккаунт
        5. Проверяем количество резерва
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        batch_of_products = ProductFactory.create_batch(5)
        response = self.client.patch(self.annulment_url)
        list_of_reserved

