from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base

if TYPE_CHECKING:
    from core.models import Order
    from core.models import OrderItem


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    stock_quantity: Mapped[int] = mapped_column(default=0, server_default='0')

    orders: Mapped[List['Order']] = relationship(
        secondary='order_item',
        back_populates='products',
    )
    orders_details: Mapped[List['OrderItem']] = relationship(
        back_populates='product',
    )
