from datetime import datetime

from app.utils.book import Book

class Library:
    def __init__(self):
        self.books = {}
        self.borrowed_books = {}  # To track borrowed books with due dates
        self.users = {}  # A dictionary to hold users for authentication
        self.admins = {}  # A dictionary to hold admins for authentication

    def add_book(self, book: Book):
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

    def borrow_book(self, book_id, user_id):
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
                print(f"User '{user_id}' has borrowed the book '{book.title}'")
                print(f"Due date: {due_date.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Sorry, '{book.title}' is currently unavailable.")
        else:
            print("Book not found!")

    def return_book(self, book_id, user_id):
        if book_id in self.borrowed_books and self.borrowed_books[book_id]["user_id"] == user_id:
            book = self.books[book_id]
            book.quantity += 1
            book.status = "Available"
            del self.borrowed_books[book_id]
            print(f"Thank you, user '{user_id}', for returning the book '{book.title}'")
        else:
            print("You did not borrow this book or the book is not found.")

    def search_book(self, title=None, category=None):
        found_books = [book for book in self.books.values() if
                       (title and title.lower() in book.title.lower()) or
                       (category and category.lower() in book.category.lower())]
        if found_books:
            print("Found books:")
            for book in found_books:
                print(book)
        else:
            print("No books found matching the search criteria.")

    def register_user(self):
        user_id = input("Enter your user ID: ")
        if user_id in self.users:
            print(f"User '{user_id}' is already registered.")
            return

        full_name = input("Enter full name: ")
        email = input("Enter email address: ")
        phone = input("Enter phone number: ")
        address = input("Enter your address: ")
        user_type = input("Enter user type (Student, Faculty, Staff, etc.): ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")

        # Convert date of birth to datetime object
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        membership_status = input("Enter membership status (Active/Inactive): ")

        # Create User object and store it
        user = User(user_id, full_name, email, phone, address, user_type, dob, membership_status)
        self.users[user_id] = user
        print(f"User '{full_name}' with ID '{user_id}' registered successfully!")

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

    def admin_login(self, admin_id, password):
        if admin_id in self.admins and self.admins[admin_id].password == password:
            print(f"Admin '{admin_id}' logged in successfully.")
            return self.admins[admin_id]
        else:
            print("Invalid Admin ID or Password.")
            return None

    def add_admin(self, admin_id, full_name, email, phone, password):
        if admin_id in self.admins:
            print(f"Admin ID '{admin_id}' already exists.")
        else:
            admin = Admin(admin_id, full_name, email, phone, password)
            self.admins[admin_id] = admin
            print(f"Admin '{full_name}' with ID '{admin_id}' added successfully!")