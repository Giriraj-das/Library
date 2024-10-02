from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings
from main import main_app
from models import db_helper, Base

async_engine = create_async_engine(url=settings.db_test.url, echo=settings.db_test.echo)
async_session = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False, expire_on_commit=False)


@pytest_asyncio.fixture(loop_scope='session', autouse=True)
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        await session.begin()
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


main_app.dependency_overrides[db_helper.scoped_session_dependency] = get_async_session


@pytest_asyncio.fixture(loop_scope='session', autouse=True)
async def async_client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url='http://test/') as async_client:
        yield async_client
