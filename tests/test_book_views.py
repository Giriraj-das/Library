from datetime import date

import pytest
from httpx import AsyncClient

from .test_data import CREATE_BOOK_VALUES

# make all test mark with `asyncio`
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('title, description, author_id, available_copies, expected_status_code', CREATE_BOOK_VALUES)
async def test_create_book(
        async_client: AsyncClient,
        author_payload: dict[str: str | date],
        title: str,
        description: str,
        author_id: int,
        available_copies: int,
        expected_status_code: int,
):
    create_response = await async_client.post('/authors', json=author_payload)
    assert create_response.status_code == 201
    author = create_response.json()

    payload = {
        'title': title,
        'description': description,
        'author_id': author_id,
        'available_copies': available_copies,
    }
    response = await async_client.post('/books', json=payload)

    assert response.status_code == expected_status_code
    data = response.json()
    if expected_status_code == 201:
        assert data['title'] == title
        assert data['description'] == description
        assert data['author_id'] == author_id
        assert data['available_copies'] == available_copies
        assert data['author']['first_name'] == author['first_name']
        assert data['author']['last_name'] == author['last_name']
        assert 'id' in data
    elif expected_status_code == 422:
        assert 'detail' in data
