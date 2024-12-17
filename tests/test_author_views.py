import pytest

from .test_data import CREATE_AUTHOR_VALUES

# make all test mark with `asyncio`
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('first_name, last_name, birth_date, expected_status_code', CREATE_AUTHOR_VALUES)
async def test_create_author(async_client, author_payload, first_name, last_name, birth_date, expected_status_code):
    response = await async_client.post('/authors', json=author_payload)
    assert response.status_code == 201

    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'birth_date': birth_date,
    }
    response = await async_client.post('/authors', json=payload)

    assert response.status_code == expected_status_code

    data = response.json()
    if expected_status_code == 201:
        assert data['first_name'] == first_name
        assert data['last_name'] == last_name
        assert data['birth_date'] == birth_date
        assert 'id' in data
    elif expected_status_code == 400:
        assert data['detail'] == 'Author already exists!'
    elif expected_status_code == 422:
        assert 'detail' in data


async def test_get_authors(async_client, authors_payload):
    for author in authors_payload:
        response = await async_client.post('/authors', json=author)
        assert response.status_code == 201
    
    response = await async_client.get('/authors')
    assert response.status_code == 200

    authors = response.json()
    assert isinstance(authors, list)
    assert len(authors) == len(authors_payload)

    for author in authors:
        assert 'id' in author
        assert 'first_name' in author
        assert 'last_name' in author

    for payload in authors_payload:
        assert any(
            author['first_name'] == payload['first_name']
            and author['last_name'] == payload['last_name']
            for author in authors
        )


async def test_get_author(async_client, author_payload):
    create_response = await async_client.post('/authors', json=author_payload)
    assert create_response.status_code == 201
    created_author = create_response.json()

    response = await async_client.get(f'/authors/{created_author["id"]}')
    assert response.status_code == 200

    data = response.json()
    assert data['first_name'] == created_author['first_name']
    assert data['last_name'] == created_author['last_name']
    assert data['birth_date'] == created_author['birth_date']
    assert data['id'] == created_author['id']


async def test_update_author(async_client, author_payload):
    create_response = await async_client.post('/authors', json=author_payload)
    assert create_response.status_code == 201
    created_author = create_response.json()

    updated_payload = {'first_name': 'Lev', 'last_name': 'Tolstoy'}
    response = await async_client.put(f'/authors/{created_author['id']}', json=updated_payload)
    assert response.status_code == 200

    updated_author = response.json()
    assert updated_author['first_name'] == updated_payload['first_name']
    assert updated_author['last_name'] == updated_payload['last_name']
    assert updated_author['birth_date'] is None
    assert updated_author['id'] == created_author['id']


async def test_delete_author(async_client, author_payload):
    create_response = await async_client.post('/authors', json=author_payload)
    assert create_response.status_code == 201
    created_author = create_response.json()

    response = await async_client.delete(f'/authors/{created_author['id']}')
    assert response.status_code == 204

    get_response = await async_client.get(f'/authors/{created_author['id']}')
    assert get_response.status_code == 404
