from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, validator
from typing import List
from enum import Enum
from string import punctuation

class User_type(str, Enum):
    student = "Student"
    admin = "Admin"
    staff = "Staff"
    parent = "Parent"

class UserModel(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr
    password: str
    phone: constr(regex=r'^\d{3}-\d{3}-\d{4}$')  # Phone number in format XXX-XXX-XXXX
    address: str
    user_type: User_type
    dob: datetime
    membership_status: str = "Active"
    borrowed_books_history: List[str] = []  # To keep track of books a user has borrowed

    # Adding a custom validator for membership status
    @validator("membership_status")
    def check_membership_status(cls, value):
        if value not in ["Active", "Inactive"]:
            raise ValueError("Membership status must be 'Active' or 'Inactive'.")
        return value

    @validator("password")
    def check_password(cls, value):

        exceptions = []

        if len(value) < 8:
            exceptions.append("Password must be greater that 8 charaters log")

        is_special_c = False
        for c in value:
            if c in punctuation:
                is_special_c = True
                break
        if not is_special_c:
            exceptions.append("Password must contain at least one special character")

        is_upper_l = False
        for l in value:
            if l.isupper():
                is_upper_l = True
                break
        if not is_upper_l:
            exceptions.append("Password must contain at least one uppercase character")

        if exceptions:
            raise ValueError(' \n'.join(exceptions))


    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models, if needed.

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.full_name}, Email: {self.email}, Phone: {self.phone}, " \
               f"Address: {self.address}, User Type: {self.user_type}, Date of Birth: {self.dob}, " \
               f"Membership Status: {self.membership_status}"