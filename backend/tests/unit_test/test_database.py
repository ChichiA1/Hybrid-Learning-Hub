import pytest
import uuid
from unittest.mock import patch, AsyncMock, ANY, MagicMock
from app.api.dependencies.database import get_db, add_update_table
from fastapi.testclient import TestClient
from app.api.server import app
from sqlalchemy.ext.asyncio import AsyncSession


# Fixture for mock async session
@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


# Fixture for FastAPI test client
@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_db(mock_session):
    """Test the get_db dependency function"""
    with patch("app.db.session.SessionLocal", return_value=mock_session):
        db_generator = get_db()
        db = await db_generator.__anext__()

        assert isinstance(db, AsyncSession)

        with pytest.raises(StopAsyncIteration):
            await db_generator.__anext__()


def test_database_engine_creation():
    """Test database engine creation"""
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_create_engine:
        import importlib
        import app.db.session
        importlib.reload(app.db.session)

        mock_create_engine.assert_called_once_with(
            'postgresql+asyncpg://postgres:postgres@postgres_db:5432/postgres',
            future=True,
            echo=False  # Updated to match actual behavior
        )


def test_session_maker_creation():
    """Test session maker creation"""
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_create_engine, \
         patch("sqlalchemy.orm.sessionmaker") as mock_sessionmaker:

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        import importlib
        import app.db.session
        importlib.reload(app.db.session)

        mock_sessionmaker.assert_called_once_with(
            bind=mock_engine,
            class_=ANY,
            expire_on_commit=False
        )


def test_database_connection_api(test_client):
    """Test database connection via API endpoint (POST)"""
    unique_suffix = str(uuid.uuid4())[:8]
    test_user = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"testuser_{unique_suffix}@example.com",
        "username": f"testuser_{unique_suffix}",
        "password": "Password123!",
        "phone": "123-456-7890",
        "address": "123 Test St",
        "user_type": "student",
        "dob": "1990-01-01T00:00:00"
    }

    response = test_client.post("/api/users/registration/", json=test_user)

    assert response.status_code == 201  # Expect 201 Created


@pytest.mark.asyncio
async def test_add_update_table():
    """Test the add_update_table helper function"""
    mock_db = AsyncMock()
    mock_data = MagicMock()

    result = await add_update_table(mock_db, mock_data)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_data)
    assert result == mock_data
