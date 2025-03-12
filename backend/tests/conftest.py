import pytest
from fastapi.testclient import TestClient
from app import app
# import databases
from unittest import mock
# import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


# Database connection setup for tests
@pytest.fixture(scope="module")
def test_db():
    # Setup PostgreSQL connection for testing
    TEST_DATABASE_URL = "postgresql://user:password@localhost/testdb"
    engine = create_engine(TEST_DATABASE_URL)
    metadata = MetaData()

    # Create tables for testing
    metadata.create_all(engine)

    # Create a session to interact with the test database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    yield db  # Provide the session for the test

    db.close()  # Close after tests


# Test client setup for FastAPI
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# Mocking a database call (if needed)
@pytest.fixture
def mock_db(mocker):
    mocker.patch('app.database', return_value=mock.Mock())
    return mock.Mock()
