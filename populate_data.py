import asyncio
from datetime import datetime, date

from core.models import db_helper, Author, Book, Borrow

authors_data = [
    {"first_name": "George", "last_name": "Orwell", "birth_date": date(1903, 6, 25)},
    {"first_name": "Harper", "last_name": "Lee", "birth_date": date(1926, 4, 28)},
    {"first_name": "J.K.", "last_name": "Rowling", "birth_date": date(1965, 7, 31)},
]

books_data = [
    {"title": "1984", "description": "A dystopian novel exploring surveillance and freedom.", "author_id": 1, "available_copies": 5},
    {"title": "Animal Farm", "description": "An allegorical novella reflecting on society.", "author_id": 1, "available_copies": 3},
    {"title": "To Kill a Mockingbird", "description": "A classic novel about racial injustice.", "author_id": 2, "available_copies": 4},
    {"title": "Harry Potter and the Philosopher's Stone", "description": "The first novel in the Harry Potter series.", "author_id": 3, "available_copies": 10},
]

borrows_data = [
    {"book_id": 1, "borrower_name": "Alice", "borrow_date": datetime(2024, 12, 11), "return_date": None},
    {"book_id": 2, "borrower_name": "Bob", "borrow_date": datetime(2024, 12, 13), "return_date": datetime(2024, 12, 10)},
    {"book_id": 4, "borrower_name": "Charlie", "borrow_date": datetime(2024, 12, 15), "return_date": None},
]


async def populate_data():
    async with db_helper.session_factory() as session:
        for author_data in authors_data:
            author = Author(**author_data)
            session.add(author)
        await session.commit()

        for book_data in books_data:
            book = Book(**book_data)
            session.add(book)
        await session.commit()

        for borrow_data in borrows_data:
            borrow = Borrow(**borrow_data)
            session.add(borrow)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(populate_data())
