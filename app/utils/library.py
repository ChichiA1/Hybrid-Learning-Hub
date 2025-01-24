from typing import Optional
from datetime import datetime, timedelta
import random
from app.models import (admins, books, users)


class Library:
    def __init__(self):
        self.books = {}
        self.borrowed_books = {}  # To track borrowed books with due dates
        self.users = {}  # A dictionary to hold users for authentication
        self.admins = {}  # A dictionary to hold admins for authentication

    def add_book(self, book: books.BookModel):
        if book.book_id in self.books:
            self.books[book.book_id].quantity += book.quantity
        else:
            self.books[book.book_id] = book
        print(f"Book '{book.title}' added successfully!")

    def view_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            print("Available books in the library:")
            for book in self.books.values():
                print(book)

    def borrow_book(self, book_id: str, user_id: str):
        if user_id not in self.users:
            print("User not registered. Please register first.")
            return
        if book_id in self.books:
            book = self.books[book_id]
            if book.quantity > 0:
                book.quantity -= 1
                book.status = "Checked-out"
                due_date = datetime.now() + timedelta(days=14)  # Books are due in 14 days
                self.borrowed_books[book_id] = {"user_id": user_id, "due_date": due_date}
                self.users[user_id].borrowed_books_history.append(book_id)  # Add to user's borrowing history
                print(f"User '{user_id}' has borrowed the book '{book.title}'")
                print(f"Due date: {due_date.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                # Check if the book is reserved by others
                if book.reserved_by:
                    print(
                        f"Sorry, '{book.title}' is currently unavailable. It's reserved by {', '.join(book.reserved_by)}.")
                else:
                    print(f"Sorry, '{book.title}' is currently unavailable.")
        else:
            print("Book not found!")

    def return_book(self, book_id: str, user_id: str):
        if book_id in self.borrowed_books and self.borrowed_books[book_id]["user_id"] == user_id:
            book = self.books[book_id]
            book.quantity += 1
            book.status = "Available"
            del self.borrowed_books[book_id]
            print(f"Thank you, user '{user_id}', for returning the book '{book.title}'")
            # Check if anyone reserved the book
            if book.reserved_by:
                next_user_id = book.reserved_by.pop(0)  # First reserved user
                print(f"Book '{book.title}' is now available for user '{next_user_id}'.")

        else:
            print("You did not borrow this book or the book is not found.")

    def search_book(self, title: Optional[str] = None, author: Optional[str] = None, category: Optional[str] = None):
        found_books = [book for book in self.books.values() if
                       (title and title.lower() in book.title.lower()) or
                       (author and author.lower() in book.author.lower()) or
                       (category and category.lower() in book.category.lower())]
        if found_books:
            print("Found books:")
            for book in found_books:
                print(book)
        else:
            print("No books found matching the search criteria.")

    def register_user(self):
        now = str(datetime.now())
        rand_num = random.sample(range(100000, 999999), 1)
        user_id = f"{now.split()[0]}-{rand_num[0]}" # format -> user_ld = 2025-01-22-12345
        # if user_id in self.users:
        #     print(f"User '{user_id}' is already registered.")
        #     return

        full_name = input("Enter full name: ")
        email = input("Enter email address: ")
        password = input("Enter you password: ")
        confirm_password = input("Confirm you password: ")
        phone = input("Enter phone number (XXX-XXX-XXXX): ")
        address = input("Enter your address: ")
        user_type = input("Enter user type (Student, Admin, Staff, Parent): ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")

        if password != confirm_password:
            print("Password does not match")
            return

        # Convert date of birth to datetime object
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        membership_status = input("Enter membership status (Active/Inactive): ")

        # Use Pydantic to validate the user data
        try:
            user = users.UserModel(
                user_id=user_id,
                full_name=full_name,
                email=email,
                password=password,
                phone=phone,
                address=address,
                user_type=user_type,
                dob=dob,
                membership_status=membership_status
            )
            self.users[user_id] = user
            print(f"User '{full_name}' with ID '{user_id}' registered successfully!")
        except ValueError as e:
            print(f"Error registering user: {e}")

    def show_user_dashboard(self, user_id: str):
        if user_id not in self.users:
            print("User not found.")
            return

        user = self.users[user_id]
        print(f"User Dashboard for {user.full_name}:")
        print(f"Membership Status: {user.membership_status}")
        print("Borrowed Books History:")
        for book_id in user.borrowed_books_history:
            book = self.books.get(book_id)
            if book:
                print(f" - {book.title} (Borrowed on {self.borrowed_books[book_id]['due_date'].strftime('%Y-%m-%d')})")
        print("Reserved Books:")
        for book_id in self.books:
            book = self.books[book_id]
            if user_id in book.reserved_by:
                print(f" - {book.title} (Reserved)")

    def show_overdue_books(self):
        overdue_books = []
        for book_id, info in self.borrowed_books.items():
            if info["due_date"] < datetime.now():
                overdue_books.append(self.books[book_id])
        if overdue_books:
            print("Overdue books:")
            for book in overdue_books:
                print(f"{book.title} (Due Date: {self.borrowed_books[book.book_id]['due_date']})")
        else:
            print("No overdue books.")

    def admin_login(self, admin_id: str, password: str):
        if admin_id in self.admins and self.admins[admin_id].password == password:
            print(f"Admin '{admin_id}' logged in successfully.")
            return self.admins[admin_id]
        else:
            print("Invalid Admin ID or Password.")
            return None

    def add_admin(self, admin_id: str, full_name: str, email: str, phone: str, password: str):
        if admin_id in self.admins:
            print(f"Admin ID '{admin_id}' already exists.")
        else:
            try:
                admin = admins.AdminModel(admin_id=admin_id, full_name=full_name, email=email, phone=phone, password=password)
                self.admins[admin_id] = admin
                print(f"Admin '{full_name}' with ID '{admin_id}' added successfully!")
            except ValueError as e:
                print(f"Error adding admin: {e}")


if __name__ == '__main__':
    pass