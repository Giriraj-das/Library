import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import func, Enum, SmallInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models import Base

if TYPE_CHECKING:
    from core.models import Product
    from core.models import OrderItem


class OrderStatus(enum.Enum):
    in_process = 'в процессе'
    shipped = 'отправлен'
    delivered = 'доставлен'


class Order(Base):
    status: Mapped[str] = mapped_column(
        Enum(OrderStatus, values_callable=lambda obj: [e.value for e in obj], name='order_status_enum'),
        default=OrderStatus.in_process.value,
        server_default=OrderStatus.in_process.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )

    products: Mapped[List['Product']] = relationship(
        secondary='order_item',
        back_populates='orders',
    )
    products_details: Mapped[List['OrderItem']] = relationship(
        back_populates='order'
    )
