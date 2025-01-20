from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, validator


# Pydantic Model for User
class UserModel(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr
    phone: constr(regex=r'^\d{3}-\d{3}-\d{4}$')  # Phone number in format XXX-XXX-XXXX
    address: str
    user_type: str
    dob: datetime
    membership_status: str = "Active"
    borrowed_books_history: List[str] = []  # To keep track of books a user has borrowed

    # Adding a custom validator for membership status
    @validator("membership_status")
    def check_membership_status(cls, value):
        if value not in ["Active", "Inactive"]:
            raise ValueError("Membership status must be 'Active' or 'Inactive'.")
        return value

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models, if needed.

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.full_name}, Email: {self.email}, Phone: {self.phone}, " \
               f"Address: {self.address}, User Type: {self.user_type}, Date of Birth: {self.dob}, " \
               f"Membership Status: {self.membership_status}"