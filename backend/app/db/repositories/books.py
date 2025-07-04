from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.orm_model.book import Book
from app.models.books import BookModel, BookStatus
from sqlalchemy.exc import SQLAlchemyError
from app.api.dependencies.database import add_update_table
import logging

# Setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BookRepository:
    """"
    All database actions associated with the Books resource
    """

    # The retrieve_book_quantity function to get the quanty by book_id from DB
    async def retrieve_book_quantity(self, db: AsyncSession, book_id: str) -> Optional[Book]:
        try:
            result = await db.execute(select(Book).filter(Book.book_id == book_id))

            # result is an instance of sqlalchemy.engine.Result
            # scalar_one_or_none() will return the first result or None
            book = result.scalar_one_or_none()

            return book  # Return the quantity of the book

        except (SQLAlchemyError, Exception) as e:
            # Handle any SQLAlchemy-related or unexpected errors
            logger.error(f"Error retrieving book quantity in the database: {e}")
            raise  # Re-raise the exception so the caller knows something went wrong

    # The add_book function to add books and commit to the DB
    async def add_book(self, db: AsyncSession, book: BookModel):
        try:
            # find out if book exist in the database and quantity there is
            book_in_bd = await self.retrieve_book_quantity(db, book.book_id)
            # add current quantity to the added quantity to make the new quantity if book exist in DB
            if book_in_bd is None:
                book_data = book.dict()
                book_data.update({
                    'status': BookStatus.available
                })
                # Create new Book instance
                db_book = Book(**book_data)
                # This stages db_book object to be added to the database, not asynchronous,
                # local opertation that happens in memory
                db.add(db_book)
                db_book = await add_update_table(db, db_book)
                return db_book.to_dict()
            else:
                book_in_bd.quantity = book_in_bd.quantity + book.quantity
                book_in_bd = await add_update_table(db, book_in_bd)
                return book_in_bd.to_dict()
        except (SQLAlchemyError, Exception) as e:
            # Handle any SQLAlchemy-related or unexpected errors
            logger.error(f"Error retrieving book quantity in the database: {e}")
            raise  # Re-raise the exception so the caller knows something went wrong


book_repo = BookRepository()
