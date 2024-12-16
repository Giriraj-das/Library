from pydantic import BaseModel

from author.schemas import AuthorNameSchema


class BookBaseSchema(BaseModel):
    title: str


class BookCreateSchema(BookBaseSchema):
    description: str | None = None
    author_id: int
    available_copies: int


class BooksSchema(BookBaseSchema):
    id: int


class BookUpdateSchema(BookCreateSchema):
    pass


class BookUpdatePartialSchema(BookCreateSchema):
    title: str | None = None
    author_id: int | None = None
    available_copies: int | None = None


class BookSchema(BookCreateSchema):
    id: int
    author: AuthorNameSchema


class BookTitleAuthorNameSchema(BookBaseSchema):
    author: AuthorNameSchema
