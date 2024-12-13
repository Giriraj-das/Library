from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, relationship
from models import Base

if TYPE_CHECKING:
    from models import Book


class Author(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]

    books: Mapped[list['Book']] = relationship(back_populates='author')
