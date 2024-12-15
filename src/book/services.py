from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from author import crud as author_crud
from book import crud
from book.schemas import BookCreateSchema, BookUpdateSchema
from core.models import db_helper, Book, Author
from utils import CustomException


async def create_book(
        book_data: BookCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Book:
    author_id: int = book_data.author_id
    author: Author | None = await author_crud.get_author(session=session, author_id=author_id)
    if not author:
        raise CustomException.http_404(detail=f'Author {author_id} not found!')

    return await crud.create_book(session=session, book_data=book_data)


async def get_books(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Book]:
    return await crud.get_books(session=session)


async def get_book(
        book_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Book:
    book: Book | None = await crud.get_book(session=session, book_id=book_id)
    if book:
        return book
    raise CustomException.http_404(detail=f'Book {book_id} not found!')


async def update_book(
        book_data: BookUpdateSchema,
        book: Book = Depends(get_book),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Book:
    return await crud.update_book(session=session, book=book, book_data=book_data)


async def delete_book(
        book: Book = Depends(get_book),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_book(session=session, book=book)
