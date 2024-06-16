import pytest
from dev.models import SalesMan
from factories import SalesManFactory
from pytest_factoryboy import register

register(SalesManFactory)

@pytest.mark.parametrize(
    "name, email, phone_no, address, validity", 
    [
        {"Jayesh", "jay@email.com", 23434234324, "abcedefghijklmnopqrestuvwxyz", True},
        {"Mahesh", "mahesh@email.com", 958290340, "qpoierua;ldkjf.z,dfn", True}
    ]
)
def test_model_with_parameters(db, sales_man_factory, name, email, phone_no, address, validity):
    sales_man = sales_man_factory(
        name = name,
        email = email,
        phone_no = phone_no,
        address = address
    )
    print(sales_man.email)
    assert SalesMan.objects.filter(email=sales_man.email).count() == 1
