from datetime import date

from pydantic import BaseModel


class AuthorBaseSchema(BaseModel):
    first_name: str
    last_name: str


class AuthorCreateSchema(AuthorBaseSchema):
    birth_date: date | None


class AuthorsSchema(AuthorBaseSchema):
    id: int


class AuthorUpdateSchema(AuthorCreateSchema):
    pass


class AuthorUpdatePartialSchema(AuthorCreateSchema):
    first_name: str | None
    last_name: str | None


class AuthorSchema(AuthorCreateSchema):
    id: int


class AuthorNameSchema(AuthorBaseSchema):
    pass
