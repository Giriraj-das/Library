from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author
from author.schemas import AuthorCreateSchema, AuthorUpdateSchema, AuthorUpdatePartialSchema


async def create_author(session: AsyncSession, author_data: AuthorCreateSchema) -> Author:
    author = Author(**author_data.model_dump())
    session.add(author)
    await session.commit()
    return author


async def get_authors(session: AsyncSession) -> list[Author]:
    stmt = select(Author).order_by(Author.last_name)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_author(session: AsyncSession, author_id: int) -> Author | None:
    return await session.get(Author, author_id)


async def update_author(
        session: AsyncSession,
        author: Author,
        author_data: AuthorUpdateSchema | AuthorUpdatePartialSchema,
        partial: bool = False,
) -> Author:
    for name, value in author_data.model_dump(exclude_unset=partial).items():
        setattr(author, name, value)
    await session.commit()
    return author


async def delete_author(session: AsyncSession, author: Author) -> None:
    await session.delete(author)
    await session.commit()
