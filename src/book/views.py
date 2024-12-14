from fastapi import APIRouter, Depends, status

from book.schemas import BookSchema, BooksSchema
from book import services
from core.config import settings
from core.models import Book

router = APIRouter(prefix=settings.prefix.book, tags=['Books'])


@router.post('', response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book = Depends(services.create_book)):
    return book


@router.get('', response_model=list[BooksSchema])
async def get_books(books: Book = Depends(services.get_books)):
    return books


@router.get('/{book_id}', response_model=BookSchema)
async def get_book(book: Book = Depends(services.get_book)):
    return book


@router.put('/{book_id}', response_model=BookSchema)
async def update_book(book: Book = Depends(services.update_book)):
    return book


@router.delete(
    '/{book_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(services.delete_book)]
)
async def delete_book() -> None:
    pass
