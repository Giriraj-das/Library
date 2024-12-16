from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models import Base

if TYPE_CHECKING:
    from core.models import Book


class Author(Base):
    __table_args__ = (UniqueConstraint('first_name', 'last_name'),)

    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date] = mapped_column(nullable=True)

    books: Mapped[list['Book']] = relationship(back_populates='author')
