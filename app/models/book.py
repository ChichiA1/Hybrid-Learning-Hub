from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Optional


# Pydantic Model for Book
class BookModel(BaseModel):
    title: str
    author: str
    book_id: str
    quantity: int
    category: str
    status: str = "Available"  # Default status is Available
    due_date: Optional[datetime] = None  # Optional, only for borrowed books
    reviews: List[str] = []
    reserved_by: List[str] = []  # Users who have reserved this book

    # Adding a custom validator for book status
    @validator("status")
    def check_status(cls, value):
        if value not in ["Available", "Checked-out"]:
            raise ValueError("Status must be 'Available' or 'Checked-out'.")
        return value

    class Config:
        orm_mode = True

    def __str__(self):
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Category: {self.category}, " \
               f"Quantity: {self.quantity}, Status: {self.status}"

    def add_review(self, review: str):
        self.reviews.append(review)

    def reserve(self, user_id: str):
        if user_id not in self.reserved_by:
            self.reserved_by.append(user_id)