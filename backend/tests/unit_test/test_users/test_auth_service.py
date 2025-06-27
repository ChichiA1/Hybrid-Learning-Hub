# import pytest
from app.models.users import UserPasswordUpdate
from app.services.authentication import auth_service


class TestAuthService:
    def test_create_hashed_password(self):
        """Test creating a hashed password"""
        plaintext_password = "Password123!"  # Example plaintext password

        # Call the method to create the hashed password
        result = auth_service.create_hashed_password(plaintext_password=plaintext_password)

        # Assertions to ensure the result is correct
        assert isinstance(result, UserPasswordUpdate)  # Ensure it's an instance of UserPasswordUpdate
        assert result.password is not None  # Ensure the password field is not None
        assert result.password != plaintext_password  # Ensure the hashed password is not the same as the plaintext
        assert len(result.password) > 0  # Ensure the hashed password has a length greater than 0
