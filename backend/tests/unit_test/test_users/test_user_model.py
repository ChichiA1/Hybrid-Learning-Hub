import pytest
from datetime import datetime, timedelta
from app.models.users import UserModel, User_type


class TestUserModel:
    def test_valid_user_model(self):
        """Test creating a valid user model"""
        user = UserModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="Password123!",
            phone="123-456-7890",
            address="123 Test St",
            user_type=User_type.student,
            dob=datetime.now() - timedelta(days=365 * 20)
        )

        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.password == "Password123!"
        assert user.phone == "123-456-7890"
        assert user.user_type == User_type.student

    def test_password_validator_too_short(self):
        """Test password validator with a too short password"""
        with pytest.raises(ValueError) as excinfo:
            UserModel(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                username="testuser",
                password="Pass!",  # Too short
                phone="123-456-7890",
                address="123 Test St",
                user_type=User_type.student,
                dob=datetime.now() - timedelta(days=365 * 20)
            )

        assert "Password must be greater that 8 charaters log" in str(excinfo.value)

    def test_password_validator_no_special_char(self):
        """Test password validator with no special character"""
        with pytest.raises(ValueError) as excinfo:
            UserModel(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                username="testuser",
                password="Password123",  # No special char
                phone="123-456-7890",
                address="123 Test St",
                user_type=User_type.student,
                dob=datetime.now() - timedelta(days=365 * 20)
            )

        assert "Password must contain at least one special character" in str(excinfo.value)

    def test_password_validator_no_uppercase(self):
        """Test password validator with no uppercase character"""
        with pytest.raises(ValueError) as excinfo:
            UserModel(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                username="testuser",
                password="password123!",  # No uppercase
                phone="123-456-7890",
                address="123 Test St",
                user_type=User_type.student,
                dob=datetime.now() - timedelta(days=365 * 20)
            )

        assert "Password must contain at least one uppercase character" in str(excinfo.value)

    def test_invalid_phone_format(self):
        """Test phone validator with invalid format"""
        with pytest.raises(ValueError) as excinfo:
            UserModel(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                username="testuser",
                password="Password123!",
                phone="1234567890",  # Invalid format
                address="123 Test St",
                user_type=User_type.student,
                dob=datetime.now() - timedelta(days=365 * 20)
            )

        assert "phone" in str(excinfo.value)
        assert "regex" in str(excinfo.value)

    def test_invalid_email_format(self):
        """Test email validator with invalid format"""
        with pytest.raises(ValueError) as excinfo:
            UserModel(
                first_name="Test",
                last_name="User",
                email="invalid-email",  # Invalid format
                username="testuser",
                password="Password123!",
                phone="123-456-7890",
                address="123 Test St",
                user_type=User_type.student,
                dob=datetime.now() - timedelta(days=365 * 20)
            )

        assert "email" in str(excinfo.value)
