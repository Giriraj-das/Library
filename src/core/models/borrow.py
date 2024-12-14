from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


if TYPE_CHECKING:
    from core.models import Book


class Borrow(Base):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    borrower_name: Mapped[str]
    borrow_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
    return_date: Mapped[datetime]

    book: Mapped['Book'] = relationship(back_populates='borrows')
