from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from enum import Enum
from string import punctuation
# from app.models.token import AccessToken


class User_type(str, Enum):
    student = "student"
    admin = "admin"
    staff = "staff"
    parent = "parent"


# Pydantic Model for User
class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    phone: constr(regex=r'^\d{3}-\d{3}-\d{4}$')
    address: str
    user_type: User_type
    dob: datetime

    # Adding a custom validator for password
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

        is_upper_c = False
        for c in value:
            if c.isupper():
                is_upper_c = True
                break
        if not is_upper_c:
            exceptions.append("Password must contain at least one uppercase character")

        if exceptions:
            raise ValueError(' \n'.join(exceptions))

        return value

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models, if needed.

    def __str__(self):
        return f"first_name: {self.first_name}, last_name: {self.last_name}, Email: {self.email}, " \
               f"Phone: {self.phone}, Address: {self.address}, User Type: {self.user_type}," \
               f"Date of Birth: {self.dob}, " \



class Membership_status(str, Enum):
    active = "active"
    inactive = "inactive"


class UserRenewal(BaseModel):
    membership_status: Membership_status = Membership_status.active
    renewal: datetime


class UserPasswordUpdate(BaseModel):
    """
    Users can create or change their password
    """
    password: constr(min_length=8, max_length=100)


# UserPublic will inherit from UserModel but make password optional and exclude it in response serialization
class UserPublic(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    phone: constr(regex=r'^\d{3}-\d{3}-\d{4}$')
    address: str
    user_type: User_type
    dob: datetime
    access_token: Optional[str] = None
