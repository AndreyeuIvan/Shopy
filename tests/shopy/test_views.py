from decimal import Decimal

from django.urls import reverse

from tests.shopy.factories import ProductFactory, ReservedFactory
from tests.shopy.base import BaseUserTest
from shopy.models import Reserved, Account, Product


class BasketViewSetTestCase(BaseUserTest):
    """
    TO-DO list:
    1. Test for Get Request +
    2. Test for Patch Request +
    3. Test for POST Request +
    4. Test for PUT Request +
    5. Test for DELETE Request
    """

    def test_get_list_method_without_auth_failed(self):
        """
        We are trying to get access to the list of values from Reserve module.
        Without an authentication.
        Result: failed
        """
        response = self.client.get(self.basket_url)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_get_list_method_success(self):
        """
        We are trying to get access to the list of values from Reserve module.
        With an authentication. And compare first value created by us
        with the first value from response.
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        products = ReservedFactory.create_batch(5, user=self.user)
        response = self.client.get(self.basket_url)
        self.assertEqual(
            len(response.data),
            Reserved.objects.filter(user=response.wsgi_request.user).count(),
        )
        self.assertEqual(
            response.data[1].get("id"), Reserved.objects.get(id=products[0].id).id
        )
        self.assertEqual(
            response.data[1].get("number_of_units"),
            Reserved.objects.get(id=products[0].id).number_of_units,
        )
        self.assertEqual(
            response.data[1].get("product"),
            Reserved.objects.get(id=products[0].id).product.id,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_method_without_auth_failed(self):
        """
        We are trying to create an object by using post request.
        Without an authentication.
        Result: failed
        """

        data = {"product": 1, "number_of_units": 3}
        response = self.client.post(self.basket_url, data=data)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_method_success(self):
        """
        We are trying to create an object by using post request for
        Reserve module.
        With an authentication, it has been provided.
        And compare creted value
        with a first value from response.
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 1, "number_of_units": 3}
        products_before_request = Reserved.objects.filter(user=self.user).count()
        response = self.client.post(self.basket_url, data=data)
        products_after_request = Reserved.objects.filter(
            user=response.wsgi_request.user
        ).count()
        self.assertNotEqual(products_before_request, products_after_request)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_method_check_validor_negative_value_failed(self):
        """
        We are trying to create an object by using post request for
        Reserve module. Number_of_units will be -1.
        With an authentication, it has been provided.
        And compare creted value
        with a first value from response.
        Result: failed
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 1, "number_of_units": -1}
        response = self.client.post(self.basket_url, data=data)
        self.assertEqual(
            "".join(response.data["number_of_units"]),
            "Ensure this value is greater than or equal to 0.",
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_method_check_validor_more_than_stock_failed(self):
        """
        We are trying to create an object by using post request for
        Reserve module. Number_of_units will be more that stock in
        Products module.
        With an authentication, it has been provided.
        And compare creted value
        with a first value from response.
        Result: failed
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 1}
        stock_of_product = Product.objects.get(id=data["product"])
        data.update({"number_of_units": stock_of_product.number_of_units + 1})
        response = self.client.post(self.basket_url, data=data)
        self.assertEqual(
            "".join(response.data["number_of_units"]), "Please increase you stock value"
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_put_method_without_auth_failed(self):
        """
        We are trying to rewrite an object by using put request for
        Reserve module.
        Without an authentication.
        Result: failed
        """
        data = {"product": 1, "number_of_units": 1}
        response = self.client.put(self.basket_url, data=data)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_put_method_success(self):
        """
        We are trying to rewrite an object by using put request for
        Reserve module.
        With an authentication, it has been provided.
        And compare Reserved values before request, Product qty after request
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 3, "number_of_units": 1}
        old_reservation = Reserved.objects.filter(id=data["product"], user=self.user)
        new_reservation = ReservedFactory.create_batch(1, user=self.user)
        own_stock_before_request = new_reservation[0].product.number_of_units
        response = self.client.put(self.basket_url, data=data)
        own_stock_after_request = Product.objects.get(
            id=data["product"]
        ).number_of_units
        print(own_stock_after_request, own_stock_before_request)
        self.assertNotEqual(own_stock_before_request, own_stock_after_request)
        self.assertEqual(
            own_stock_before_request + data["number_of_units"], own_stock_after_request
        )
        self.assertNotEqual(old_reservation, new_reservation)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_put_method_check_validor_negative_value_failed(self):
        """
        We are trying to rewrite an object by using put request for
        Reserve module. Number_of_units will be -1.
        With an authentication, it has been provided.
        By comparing created value
        with a first value from response.
        Result: failed
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 2, "number_of_units": -1}
        response = self.client.put(self.basket_url, data=data)
        self.assertEqual(
            "".join(response.data["number_of_units"]),
            "Ensure this value is greater than or equal to 0.",
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_put_method_check_validor_more_than_stock_success(self):
        """
        We are trying to rewrite an object by using put request for
        Reserve module. Number_of_units will be more that stock in products module.
        With an authentication, it has been provided.
        By comparing created value
        with a first value from response.
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {"product": 2}
        stock_of_product = Product.objects.get(id=data["product"])
        data.update({"number_of_units": stock_of_product.number_of_units + 1})
        old_reservation = Reserved.objects.filter(id=data["product"], user=self.user)
        new_reservation = ReservedFactory.create_batch(1, user=self.user)
        own_stock_before_request = new_reservation[0].product.number_of_units
        response = self.client.put(self.basket_url, data=data)
        own_stock_after_request = Product.objects.get(
            id=data["product"]
        ).number_of_units
        self.assertNotEqual(
            str(response.data["number_of_units"]),
            "Ensure this value is greater than or equal to 0.",
        )
        self.assertEqual(
            own_stock_before_request + data["number_of_units"], own_stock_after_request
        )
        self.assertNotEqual(old_reservation, new_reservation)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_delete_method_auth_success(self):
        """
        We are trying to delete an object by using delete request for
        Reserve module.
        With an authentication, it has been provided.
        And compare Reserved values before request, Product qty after request
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        new_url = self.basket_url + str(self.reserve.product.id) + "/"
        response = self.client.delete(new_url)
        self.assertEqual(
            response.data,
            "Balance has been restored",
        )
        self.assertNotEqual(
            self.reserve.product.number_of_units,
            Product.objects.get(id=self.reserve.product.id).number_of_units,
        )
        self.assertNotEqual(
            self.reserve,
            Reserved.objects.get_queryset(),
        )
        self.assertEqual(
            self.reserve.product.number_of_units + self.reserve.number_of_units,
            Product.objects.get(id=self.reserve.product.id).number_of_units,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_delete_method_auth_failed(self):
        new_url = self.basket_url + str(self.reserve.product.id) + "/"
        response = self.client.delete(new_url)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_delete_method_no_reserved_products(self):
        """
        We are trying to delete an object by using delete request for
        Reserve module.
        With an authentication, it has been provided.
        And compare while Reserved qty, is null
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        new_url = self.basket_url + str(self.product.id) + "/"
        response = self.client.delete(new_url)
        self.assertEqual(
            response.data,
            "Fullfill your basket",
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class AnnulmentGenericAPIViewTestCase(BaseUserTest):
    """
    TO-DO list:
    1. Make test for Patch request
    2. Make test for DELETE Request
    """

    def test_patch_method_without_auth_failed(self):
        """
        We are trying rewrite values from Reserve module.
        Without an authentication.
        Result: failed
        """
        response = self.client.get(self.basket_url)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_patch_method_success(self):
        """
        We are trying to rewrite an object by using patch request for
        Reserve module.
        With an authentication, it has been provided.
        And compare Account amount value before and after request were made.
        Result: success
        """
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        data = {}
        user_amount_before_request = float(Account.objects.get(user=self.user).amount)
        queryset_of_products = Reserved.objects.filter(user=self.user)
        sum_reserved = float(sum([x.total_price for x in queryset_of_products]))
        response = self.client.patch(self.annulment_url, data=data)
        user_amount_after_request = float(Account.objects.get(user=self.user).amount)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertNotEqual(user_amount_before_request, user_amount_after_request)
        self.assertEqual(
            round(user_amount_before_request - sum_reserved, 2),
            user_amount_after_request,
        )

    def test_patch_method_failed(self):
        """
        We are trying to rewrite an object by using patch request for
        Reserve module. Reserves is null
        With an authentication, it has been provided.
        And compare Account amount value before and after request were made.
        Result: failed
        """
        self.client.post(
            reverse("login"),
            {
                "username": self.other_user.username,
                "password": self.password_other_user,
            },
        )
        response = self.client.delete(self.annulment_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.data, "There is no Reserved products.")


class PurchaseListAPIViewTestCase(BaseUserTest):
    """
    TO-DO list:
    Test Permission.
    Test Filter.
    Test Ordering.
    """

    def test_with_some_products_created_by_one_user(self):
        products = ProductFactory.create_batch(5)
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        response = self.client.get(self.search_url)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        self.assertTrue(self.product.id == response.data[0].get("id"))
        self.assertTrue(
            self.product.price_for_kilo == float(response.data[0].get("price_for_kilo"))
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(products[0].name == response.data[2].get("name"))
        self.assertTrue(products[0].id == response.data[2].get("id"))
        self.assertTrue(
            products[0].price_for_kilo == float(response.data[2].get("price_for_kilo"))
        )

    def test_product_search_get_list_of_products(self):
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        response = self.client.get(self.search_url)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        self.assertTrue(self.product.id == response.data[0].get("id"))
        self.assertTrue(
            self.product.price_for_kilo == float(response.data[0].get("price_for_kilo"))
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_product_search_get_product_by_using_filter_name_of_the_product(self):
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        filter = "name"
        url_filter = f"{self.search_url}?{filter}={self.product.name}"
        response = self.client.get(url_filter)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        self.assertTrue(self.product.id == response.data[0].get("id"))
        self.assertTrue(
            self.product.price_for_kilo == float(response.data[0].get("price_for_kilo"))
        )

    def test_product_search_get_product_by_using_filter_name_of_the_shop(self):
        self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )
        ProductFactory.create_batch(5)
        filter = "shop_name"
        url_filter = f"{self.search_url}?{filter}={self.product.shop_name}"
        response = self.client.get(url_filter)
        self.assertTrue(self.product.name == response.data[0].get("name"))
        self.assertTrue(self.product.id == response.data[0].get("id"))
        self.assertTrue(
            self.product.price_for_kilo == float(response.data[0].get("price_for_kilo"))
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

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
        response = self.client.get(url_filter)
        products.append(self.product)
        sorted_result = sorted(products, key=lambda x: x.price_for_unit)
        self.assertTrue(float(sorted_result[0].price_for_unit)) == float(
            (response.data[0].get("price_for_unit"))
        )
        self.assertTrue(sorted_result[0].name == response.data[0].get("name"))
        self.assertTrue(sorted_result[0].id == response.data[0].get("id"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

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
        response = self.client.get(url_filter)
        products.append(self.product)
        sorted_result = sorted(products, key=lambda x: x.price_for_kilo, reverse=True)
        self.assertTrue(float(sorted_result[0].price_for_kilo)) == float(
            (response.data[0].get("price_for_kilo"))
        )
        self.assertTrue(sorted_result[0].name == response.data[0].get("name"))
        self.assertTrue(sorted_result[0].id == response.data[0].get("id"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

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
        response = self.client.get(url_filter)
        products.append(self.product)

        sorted_result_first_time = sorted(
            products, key=lambda x: x.price_for_kilo, reverse=True
        )
        sorted_result_second_time = sorted(
            sorted_result_first_time, key=lambda x: x.price_for_unit, reverse=True
        )
        self.assertEqual(
            float(sorted_result_second_time[0].price_for_kilo),
            float(response.data[0].get("price_for_kilo")),
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
