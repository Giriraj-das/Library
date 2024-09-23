from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


if TYPE_CHECKING:
    from models import Order
    from models import Product


class OrderItem(Base):
    __tablename__ = 'order_item'
    __table_args__ = (UniqueConstraint('order_id', 'product_id'),)

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=1, server_default='1')

    # association between OrderItem -> Order
    order: Mapped['Order'] = relationship(
        back_populates='products_details',
    )
    # association between OrderItem -> Product
    product: Mapped['Product'] = relationship(
        back_populates='orders_details',
    )
