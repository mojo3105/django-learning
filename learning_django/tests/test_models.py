import pytest

from pytest_factoryboy import register
from factories import SalesManFactory, ProductFactory

register(SalesManFactory)
register(ProductFactory)


def test_salesman_model(sales_man_factory):
    print(sales_man_factory.name, sales_man_factory.email, sales_man_factory.phone_no, sales_man_factory.address)
    assert True

@pytest.mark.product
def test_product_model(product_factory):
    product = product_factory.build()
    print(product.name, product.price_in_dollars)
    print(product.agent)
    assert True