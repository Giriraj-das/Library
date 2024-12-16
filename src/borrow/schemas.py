from datetime import datetime

from pydantic import BaseModel

from book.schemas import BookTitleAuthorNameSchema


class BorrowBaseSchema(BaseModel):
    book_id: int
    borrower_name: str


class BorrowCreateSchema(BorrowBaseSchema):
    pass


class BorrowsSchema(BorrowBaseSchema):
    id: int
    book: BookTitleAuthorNameSchema


class BorrowReturnSchema(BaseModel):
    return_date: datetime


class BorrowSchema(BorrowCreateSchema):
    id: int
    borrow_date: datetime
    return_date: datetime | None
    book: BookTitleAuthorNameSchema
