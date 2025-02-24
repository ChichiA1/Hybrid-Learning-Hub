from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import ARRAY  # Still using ARRAY for list types (e.g., reviews)
from app.db.base import Base

# Enum for status (same as Pydantic Enum)
class BookStatusEnum(PyEnum):
    available = "available"
    checked_out = "checked-out"
    reserved = "reserved"

class Book(Base):
    __tablename__ = 'books'

    # Columns definition
    book_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    quantity = Column(Integer)
    category = Column(String)
    status = Column(Enum(BookStatusEnum), default=BookStatusEnum.available)  # Using SQLAlchemy's native Enum

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "quantity": self.quantity,
            "category": self.category,
            "status": self.status.value
        }