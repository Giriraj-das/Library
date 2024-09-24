from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import db_helper, Order
from crud import order as order_crud
from schemas.order import OrderSchema, OrderInfoNameSchema, OrderCreateSchema, OrderUpdatePartialSchema
from services.order import order_by_id

router = APIRouter(prefix=settings.prefix.order, tags=['Orders'])


@router.post('', response_model=OrderInfoNameSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
        order_data: OrderCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await order_crud.create_order_item(session=session, order_data=order_data)


@router.get('', response_model=list[OrderSchema])
async def get_orders(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await order_crud.get_orders(session=session)


@router.get('/{order_id}', response_model=OrderInfoNameSchema)
async def get_order(
        order: Order = Depends(order_by_id),
):
    return order


@router.patch("/{order_id}/status", response_model=OrderSchema)
async def update_order(
        order_data: OrderUpdatePartialSchema,
        order: Order = Depends(order_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await order_crud.update_order(
        session=session,
        order=order,
        order_data=order_data,
    )
