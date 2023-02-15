import factory

from shopy.models import Account, Product, Reserved, Shop
from tests.my_auth.factories import UserFactory


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    amount = factory.Faker("pydecimal", max_value=1000, right_digits=2)


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    name = factory.Faker("name")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    shop_name = factory.SubFactory(ShopFactory)
    unit = factory.Faker("pydecimal", min_value=0, max_value=1, right_digits=2)
    number_of_units = factory.Faker("pydecimal", min_value=1, max_value=15)
    price_for_unit = factory.Faker("pydecimal", max_value=15, right_digits=2)


class ReservedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reserved

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    number_of_units = factory.Faker("pydecimal", min_value=1, max_value=15)
