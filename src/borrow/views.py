from fastapi import APIRouter, Depends, status

from borrow.schemas import BorrowCreateSchema, BorrowsSchema, BorrowSchema
from borrow import services
from core.config import settings
from core.models import Borrow

router = APIRouter(prefix=settings.prefix.borrow, tags=['Borrows'])


@router.post('', response_model=BorrowCreateSchema, status_code=status.HTTP_201_CREATED)
async def create_borrow(borrow: Borrow = Depends(services.create_borrow)):
    return borrow


@router.get('', response_model=list[BorrowsSchema])
async def get_borrows(borrows: list[Borrow] = Depends(services.get_borrows)):
    return borrows


@router.get('/{borrow_id}', response_model=BorrowSchema)
async def get_borrow(borrow: Borrow = Depends(services.get_borrow)):
    return borrow


@router.patch('/{borrow_id}/return', response_model=BorrowSchema)
async def return_borrow(borrow: Borrow = Depends(services.return_borrow)):
    return borrow
