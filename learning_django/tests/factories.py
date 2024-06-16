import factory 
from faker import Faker
from dev.models import SalesMan, Products
import random
fake = Faker()

class SalesManFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SalesMan

    name = fake.name()
    email = fake.email()
    phone_no = fake.phone_number()
    address = fake.address()


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Products

    name = fake.name()
    price_in_dollars = round(random.random(), 2)
    agent = factory.SubFactory(SalesManFactory)
