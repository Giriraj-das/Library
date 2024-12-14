from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book
from book.schemas import BookCreateSchema, BookUpdateSchema, BookUpdatePartialSchema


async def create_book(session: AsyncSession, book_data: BookCreateSchema) -> Book:
    book = Book(**book_data.model_dump())
    session.add(book)
    await session.commit()
    return book


async def get_books(session: AsyncSession) -> list[Book]:
    stmt = select(Book).order_by(Book.title)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_book(session: AsyncSession, book_id: int) -> Book | None:
    return await session.get(Book, book_id)


async def update_book(
        session: AsyncSession,
        book: Book,
        book_data: BookUpdateSchema | BookUpdatePartialSchema,
        partial: bool = False,
) -> Book:
    for name, value in book_data.model_dump(exclude_unset=partial).items():
        setattr(book, name, value)
    await session.commit()
    return book


async def delete_book(session: AsyncSession, book: Book) -> None:
    await session.delete(book)
    await session.commit()
