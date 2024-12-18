from datetime import date
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings
from main import main_app
from core.models import db_helper, Base

async_engine = create_async_engine(url=settings.db_test.url, echo=settings.db_test.echo)


@pytest_asyncio.fixture(scope='function', autouse=True)
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()


main_app.dependency_overrides[db_helper.scoped_session_dependency] = get_async_session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def async_client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url='http://test/') as async_client:
        yield async_client


@pytest_asyncio.fixture(scope='module')
def author_payload() -> dict[str: str | date]:
    return {
        'first_name': 'Mark',
        'last_name': 'Twain',
        'birth_date': '1835-11-30',
    }


@pytest_asyncio.fixture(scope='module')
def authors_payload() -> dict[str: str]:
    return [
        {'first_name': 'Aleksandr', 'last_name': 'Pushkin'},
        {'first_name': 'George', 'last_name': 'Orwell'},
        {'first_name': 'Mark', 'last_name': 'Twain'},
    ]


@pytest_asyncio.fixture(scope='module')
def book_payload() -> dict[str: str | int]:
    return {
        'title': 'War and Peace',
        'description': 'A historical novel by Leo Tolstoy.',
        'author_id': 1,
        'available_copies': 5,
    }
