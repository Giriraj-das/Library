from pydantic import BaseModel, Field

from author.schemas import AuthorNameSchema


class BookBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)


class BookCreateSchema(BookBaseSchema):
    description: str | None = Field(None, min_length=10)
    author_id: int
    available_copies: int = Field(ge=0)  # greater than or equal


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
