import pytest
from django.urls import reverse
from dev.models import Products, SalesMan
import json

@pytest.fixture(scope='function')
def name_fixture():
    return 'Mohit'

@pytest.fixture
def product_object_fixture():
    salesman = SalesMan(name='Mohit Joshi', email='Mohit@email.com', phone_no=9874983292, 
                        address='27B, Baker Street, London, UK.')
    product = Products(name='Book', price_in_dollars=90, agent=salesman)
    return salesman, product 

def test_sample(name_fixture):
    st = f"Hello {name_fixture}"
    assert st == 'Hello Mohit'

@pytest.mark.django_db
def test_product_get(client, product_object_fixture):
    salesman, product = product_object_fixture
    salesman.save()
    product.save()
    url = reverse('products', args=[product.id])
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['name'] == 'Book'

@pytest.mark.django_db
def test_product_getl_all(client, product_object_fixture):
    salesman, product = product_object_fixture
    salesman.save()
    product.save()
    url = reverse('products')
    response = client.get(url)
    data = json.loads(response.content)
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)
        assert list(item.keys()) == ['id', 'name', 'price_in_dollars', 'agent_name', 'agent_email', 'created_at', 
                                     'updated_at']
        
@pytest.mark.django_db
def test_product_post(client, product_object_fixture):
    salesman, product = product_object_fixture
    salesman.save()
    product.save()
    url = reverse('products', args=[product.id])
    response = client.post(url)
    assert response.status_code == 400
    request_data = {'name': 'New Product', 'price_in_dollars': 50.0, 'agent_id':10}
    response = client.post(reverse('products'), data=json.dumps(request_data), content_type='application/json')
    assert response.status_code == 200
    assert list(json.loads(response.content).keys()) == ["Error"]
    # assert Products.objects.filter(name='New Product', price_in_dollars=50.0).exists() 


@pytest.mark.django_db
def test_product_put(client, product_object_fixture):
    salesman, product = product_object_fixture
    salesman.save()
    product.save()
    url = reverse('products', args=[product.id])
    request_data = {'name': 'Books', 'price_in_dollars': 50.0, 'agent_id':1}
    response = client.put(url, data=json.dumps(request_data), content_type='application/json')
    response_data = json.loads(response.content)
    print(response_data)
    assert response.status_code == 200
    assert list(response_data.keys()) == ["Success"]
    assert Products.objects.filter(name='Books').exists()

@pytest.mark.django_db
def test_product_delete(client, product_object_fixture):
    salesman, product = product_object_fixture
    salesman.save()
    product.save()
    url = reverse('products', args=[product.id])
    response = client.delete(url)
    response_data = json.loads(response.content)
    print(response_data)
    assert response.status_code == 200
    assert list(response_data.keys()) == ["Success"]