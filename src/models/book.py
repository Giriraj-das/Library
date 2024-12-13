from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base

if TYPE_CHECKING:
    from models import Author
    from models import Borrow


class Book(Base):
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    available_copies: Mapped[int] = mapped_column(default=1, server_default='1')

    author: Mapped['Author'] = relationship(back_populates='books')
    borrows: Mapped[list['Borrow']] = relationship(back_populates='book')
