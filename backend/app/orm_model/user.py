from sqlalchemy import Column, String, Integer, Enum, DateTime
from datetime import datetime
from enum import Enum as PyEnum
from app.db.base import Base


# Enums for User Type and Membership Status
class Membership_status(PyEnum):
    active = "active"
    inactive = "inactive"

class User_type(PyEnum):
    student = "student"
    faculty = "faculty"
    staff = "staff"
    parent = "parent"

# SQLAlchemy ORM model for User
class User(Base):
    __tablename__ = 'users'

    # Columns
    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # Store hashed password here
    salt = Column(String, nullable=False)  # Store salt for password hashing
    phone = Column(String)  # Store phone number as a string in the format XXX-XXX-XXXX
    address = Column(String)
    user_type = Column(Enum(User_type), default=User_type.student, nullable=False)  # Enum for user type with default
    dob = Column(DateTime, nullable=False)
    membership_status = Column(Enum(Membership_status), default=Membership_status.active, nullable=False)  # Enum for membership status
    renewal = Column(DateTime, nullable=False)  # DateTime for renewal

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "phone": self.phone,
            "address": self.address,
            "user_type": self.user_type.value,  # Convert Enum to string
            "dob": self.dob
        }

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, email={self.email})>"