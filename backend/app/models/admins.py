from pydantic import BaseModel, EmailStr, constr

# Pydantic Model for Admin
class AdminModel(BaseModel):
    admin_id: str
    full_name: str
    email: EmailStr
    phone: constr(regex=r'^\d{3}-\d{3}-\d{4}$')  # Phone number validation
    password: str  # Store the password securely (in real apps use hashed passwords)

    class Config:
        orm_mode = True

    def __str__(self):
        return f"Admin ID: {self.admin_id}, Name: {self.full_name}, Email: {self.email}, Phone: {self.phone}"