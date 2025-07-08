import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.models.users import UserModel, User_type
from app.services.authentication import AuthService
from app.db.repositories.users import UsersRepository
from app.models.books import BookModel, BookStatus
from app.api.server import app as fastapi_app


@pytest.fixture
def test_user():
    """Create a test user"""
    return UserModel(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="testuser",
        password="Password123!",
        phone="123-456-7890",
        address="123 Test St",
        user_type=User_type.student,
        dob=datetime.now() - timedelta(days=365 * 20)  # 20 years ago
    )


@pytest.fixture
def mock_db():
    """Create a mock database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def auth_service():
    """Create a real AuthService instance"""
    return AuthService()


@pytest.fixture
def user_repo():
    """Create a real UsersRepository instance"""
    return UsersRepository()


@pytest.fixture
def client():
    """Create a FastAPI test client"""
    return TestClient(fastapi_app)


@pytest.fixture
def mock_user_dict():
    """Create a mock user dictionary returned from the repository"""
    return {
        "user_id": "test-user-id",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "username": "testuser",
        "password": "hashed_password",  # This would be hashed in reality
        "phone": "123-456-7890",
        "address": "123 Test St",
        "user_type": "student",
        "dob": (datetime.now() - timedelta(days=365 * 20)).isoformat(),
        "membership_status": "active",
        "renewal": (datetime.now() + timedelta(days=365)).isoformat()
    }


@pytest.fixture
def test_book():
    return BookModel(
        title="The Art of Testing",
        author="Jane Doe",
        book_id="book-1234",
        quantity=10,
        category="Technology",
        status=BookStatus.available
    )


# @pytest.fixture
# def app():
#     """Fixture to provide the FastAPI app."""
#     return fastapi_app
#
#
# @pytest.fixture
# def client(app):
#     from starlette.testclient import TestClient
#     return TestClient(app)
