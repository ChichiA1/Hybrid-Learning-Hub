from datetime import datetime

class Book:
    def __init__(self, title, author, book_id, quantity, category):
        now = datetime.now()
        self.title = title
        self.author = author
        self.book_id = str(now).split()[0] + "-" + str(now).split(".")[-1]
        self.quantity = quantity
        self.category = category
        self.status = "Available"  # New Book status: Available/Checked-out
        self.due_date = None
        self.reviews = []

    def __str__(self):
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Category: {self.category}, Quantity: {self.quantity}, Status: {self.status}"

    def add_review(self, review):
        self.reviews.append(review)

    def show_reviews(self):
        if self.reviews:
            print(f"Reviews for '{self.title}':")
            for idx, review in enumerate(self.reviews, 1):
                print(f"{idx}. {review}")
        else:
            print("No reviews yet for this book.")