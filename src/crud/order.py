from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import Order, OrderItem
from schemas.order import OrderCreateSchema, OrderUpdatePartialSchema


async def create_order(session: AsyncSession, status: str | None) -> Order:
    order = Order(status=status)
    session.add(order)
    await session.commit()
    # await session.refresh(order)
    return order


async def create_order_item(session: AsyncSession, order_data: OrderCreateSchema):
    order = await create_order(session, status=order_data.status)
    order_items = [
        OrderItem(
            order_id=order.id,
            product_id=product_data.id,
            quantity=product_data.quantity,
        ) for product_data in order_data.products_details
    ]
    session.add_all(order_items)
    await session.commit()

    # for return
    order = await session.scalar(
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.products_details).selectinload(OrderItem.product),
        ),
    )
    return order


async def get_orders(session: AsyncSession) -> list[Order]:
    stmt = select(Order).order_by(Order.id)
    results = await session.scalars(stmt)
    return list(results)


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    order = await session.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.products_details).joinedload(OrderItem.product),
        ).order_by(Order.id),
    )
    return order


async def update_order(session: AsyncSession, order: Order, order_data: OrderUpdatePartialSchema) -> Order:
    for name, value in order_data.model_dump(exclude_unset=True).items():
        setattr(order, name, value)
    await session.commit()
    return order
