import factory

from django.contrib.auth.hashers import make_password
from my_auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")
