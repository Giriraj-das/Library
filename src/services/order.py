from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Order
from crud import order as order_crud


async def order_by_id(
    order_id: int = Path,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Order:
    order = await order_crud.get_order(session=session, order_id=order_id)
    if order:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {order_id} not found!",
    )
