from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from borrow.schemas import BorrowCreateSchema, BorrowReturnSchema
from core.models import Borrow, Book


async def create_borrow(session: AsyncSession, borrow_data: BorrowCreateSchema) -> Borrow:
    borrow = Borrow(**borrow_data.model_dump())
    session.add(borrow)
    await session.commit()
    return borrow


async def get_borrows(session: AsyncSession) -> list[Borrow]:
    stmt = (
        select(Borrow)
        .options(selectinload(Borrow.book).selectinload(Book.author))
        .order_by(Borrow.borrow_date)
    )
    result = await session.scalars(stmt)
    return list(result.all())


async def get_borrow(session: AsyncSession, borrow_id: int) -> Borrow | None:
    stmt = (
        select(Borrow)
        .options(selectinload(Borrow.book).selectinload(Book.author))
        .where(Borrow.id == borrow_id)
    )
    return await session.scalar(stmt)


async def update_borrow(
        session: AsyncSession,
        borrow: Borrow,
        borrow_data: BorrowReturnSchema,
        partial: bool = False,
) -> Borrow:
    for name, value in borrow_data.model_dump(exclude_unset=partial).items():
        setattr(borrow, name, value)
    await session.commit()

    stmt = (
        select(Borrow)
        .options(selectinload(Borrow.book).selectinload(Book.author))
        .where(Borrow.id == borrow.id)
    )
    return await session.scalar(stmt)
