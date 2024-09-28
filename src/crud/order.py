from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from crud.product import get_product
from models import Order, OrderItem
from schemas.order import OrderCreateSchema, OrderUpdatePartialSchema


async def create_order(session: AsyncSession, status: str | None) -> Order:
    order = Order(status=status)
    session.add(order)
    await session.commit()
    return order


async def create_order_item(session: AsyncSession, order_data: OrderCreateSchema):
    # Checking product availability, and products quantity.
    for product_data in order_data.products_details:
        product = await get_product(session, product_id=product_data.id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Product: {product_data.id} does not exist.'
            )
        if product.stock_quantity < product_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Insufficient stock for product: {product.name}. '
                f'Available: {product.stock_quantity}, requested: {product_data.quantity}.'
            )

    order = await create_order(session, status=order_data.status)

    for product_data in order_data.products_details:
        product = await get_product(session, product_id=product_data.id)
        product.stock_quantity -= product_data.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_data.id,
            quantity=product_data.quantity,
        )
        session.add(order_item)

    await session.commit()

    # for return
    order = await session.scalar(
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.products_details).joinedload(OrderItem.product),
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
