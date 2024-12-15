from datetime import date

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from book import crud as book_crud
from borrow import crud
from borrow.schemas import BorrowCreateSchema, BorrowReturnSchema
from core.models import db_helper, Borrow, Book
from utils import CustomException


async def create_borrow(
        borrow_data: BorrowCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Borrow:
    book_id: int = borrow_data.book_id
    book: Book | None = await book_crud.get_book(session=session, book_id=book_id)

    if not book:
        raise CustomException.http_404(detail=f'Book {book_id} not found')
    if book.available_copies < 1:
        raise CustomException.http_400(detail='No available copies of the book')

    book.available_copies -= 1
    return await crud.create_borrow(session=session, borrow_data=borrow_data)


async def get_borrows(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Borrow]:
    return await crud.get_borrows(session=session)


async def get_borrow(
        borrow_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Borrow:
    borrow: Borrow | None = await crud.get_borrow(session=session, borrow_id=borrow_id)
    if borrow:
        return borrow
    raise CustomException.http_404(detail=f'Borrow {borrow_id} not found!')


async def return_borrow(
        borrow_data: BorrowReturnSchema,
        borrow: Borrow = Depends(get_borrow),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Borrow:
    today: date = date.today()
    return_date: date = borrow_data.return_date.date()
    if borrow.return_date:
        raise CustomException.http_400(detail='The book has been returned.')

    if return_date < borrow.borrow_date.date():
        raise CustomException.http_400(detail='Return date cannot be earlier than borrow date.')
    if return_date > today:
        raise CustomException.http_400(detail='Return date cannot be later than today.')

    book = await book_crud.get_book(session=session, book_id=borrow.book_id)
    book.available_copies += 1

    return await crud.update_borrow(
        session=session,
        borrow=borrow,
        borrow_data=borrow_data,
        partial=True,
    )
