from models.order import OrderStatus
import pytest

# make all test mark with `asyncio`
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'quantity, status, expected_status_code',
    [
        (2, OrderStatus.in_process.value, 201),  # Correct
        (2, OrderStatus.shipped.value, 201),  # Correct
        (1, OrderStatus.delivered.value, 201),  # Correct
        (3, OrderStatus.delivered.value, 400),  # Error with insufficient quantity in stock
        (1, None, 201),  # Without status
        pytest.param(1, "invalid_status", 422,
                     marks=pytest.mark.xfail(reason="invalid status")),  # Incorrect status
    ]
)
async def test_create_order(async_client, quantity, status, expected_status_code):
    product_payload = {
        'name': 'product',
        'description': 'product description',
        'price': 110,
        'stock_quantity': 2
    }
    product_response = await async_client.post('/products', json=product_payload)
    assert product_response.status_code == 201, product_response.text
    product_data = product_response.json()
    assert product_data['name'] == product_payload['name']
    assert product_data['description'] == product_payload['description']
    assert product_data['price'] == product_payload['price']
    assert product_data['stock_quantity'] == product_payload['stock_quantity']
    assert "id" in product_data
    product_data_id = product_data['id']

    payload = {
        'status': status,
        'products_details': [
            {
                'id': product_data_id,
                'quantity': quantity
            }
        ]
    }
    response = await async_client.post('/orders', json=payload)
    assert response.status_code == expected_status_code

    data = response.json()
    if response.status_code == 201:
        assert data['status'] == status or OrderStatus.in_process.value
        assert data['products_details'][0]['quantity'] == quantity
        assert data['products_details'][0]['product']['id'] == product_data['id']
        assert data['products_details'][0]['product']['name'] == product_payload['name']
    elif response.status_code == 400:
        assert 'detail' in data
        assert 'Insufficient stock' in data['detail']
