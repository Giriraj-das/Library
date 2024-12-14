from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from author import crud
from author.schemas import AuthorCreateSchema, AuthorUpdateSchema
from core.models import db_helper, Author


async def create_author(
        author_data: AuthorCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Author:
    return await crud.create_author(session=session, author_data=author_data)


async def get_authors(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Author]:
    return await crud.get_authors(session=session)


async def get_author(
        author_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Author:
    author: Author | None = await crud.get_author(session=session, author_id=author_id)
    if author:
        return author
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author {author_id} not found!",
        )


async def update_author(
        author_data: AuthorUpdateSchema,
        author: Author = Depends(get_author),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Author:
    return await crud.update_author(session=session, author=author, author_data=author_data)


async def delete_author(
        author: Author = Depends(get_author),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_author(session=session, author=author)