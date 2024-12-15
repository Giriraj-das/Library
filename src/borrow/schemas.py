from datetime import datetime

from pydantic import BaseModel, field_validator


class BorrowBaseSchema(BaseModel):
    book_id: int
    borrower_name: str


class BorrowCreateSchema(BorrowBaseSchema):
    pass


class BorrowsSchema(BorrowBaseSchema):
    id: int


class BorrowReturnSchema(BaseModel):
    return_date: datetime


class BorrowSchema(BorrowCreateSchema):
    id: int
    borrow_date: datetime
    return_date: datetime | None
