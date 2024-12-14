from pydantic import BaseModel


class BookBaseSchema(BaseModel):
    title: str


class BookCreateSchema(BookBaseSchema):
    description: str | None
    author_id: int
    available_copies: int


class BooksSchema(BookBaseSchema):
    id: int


class BookUpdateSchema(BookCreateSchema):
    pass


class BookUpdatePartialSchema(BookCreateSchema):
    title: str | None
    author_id: int | None
    available_copies: int | None


class BookSchema(BookCreateSchema):
    id: int
