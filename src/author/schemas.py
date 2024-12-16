from datetime import date

from pydantic import BaseModel, Field


class AuthorBaseSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=50)


class AuthorCreateSchema(AuthorBaseSchema):
    birth_date: date | None = None


class AuthorsSchema(AuthorBaseSchema):
    id: int


class AuthorUpdateSchema(AuthorCreateSchema):
    pass


class AuthorUpdatePartialSchema(AuthorCreateSchema):
    first_name: str | None = None
    last_name: str | None = None


class AuthorSchema(AuthorCreateSchema):
    id: int


class AuthorNameSchema(AuthorBaseSchema):
    pass
