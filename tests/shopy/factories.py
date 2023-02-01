import factory
from faker import Factory

from shopy.models import Account, Product, Reserved, Shop
from tests.my_auth.factories import UserFactory


faker = Factory.create()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    amount = faker.pyfloat(min_value=1, max_value=1500, right_digits=2)


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    name = factory.Faker("name")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    shop_name = factory.SubFactory(ShopFactory)
    unit = faker.pyfloat(min_value=0.1, max_value=1, right_digits=2)
    number_of_units = faker.pyint(min_value=1, max_value=15)
    price_for_unit = faker.pyfloat(min_value=1, max_value=15, right_digits=2)


class ReservedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reserved

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    number_of_units = faker.pyint(min_value=1, max_value=15)
