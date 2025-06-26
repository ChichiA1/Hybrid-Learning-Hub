Overview


# Hybrid-Learning-Hub
physical (bricks &amp; mortal) and online digital learning hub

## docker, Alembic and database commands

1. docker-compose exec -it fastapi-server bash
2. alembic revision --autogenerate -m "create_main_tables"
2. alembic upgrade head - whenever you update the table
3. alembic downgrade -1 - to rollback 1 migration step
4. docker-compose exec postgres_db psql -h localhost -U postgres --dbname=postgres

- \l - list all databases
- \d+ - list all tables (relations) in the current database
- \dT+ - list all enums in the current database
- \c postgres - connect to the postgres database
- \d users - describe the users table and the associated columns

- openssl rand -hex 32

# Testing Structure for FastAPI User Registration System

This document outlines the modular testing structure created for the FastAPI user registration system.

## Project Structure

```
tests/
  ├── unit_test
  |       ├── test_users                     # Test for all users endpoints and all associated models and classes
  |       |     ├── test_auth_service.py     # Tests for the authentication service
  |       |     ├── test_users_repository.py # Tests for the users repository
  |       |     ├── test_user_model.py       # Tests for the user model validation
  |       |     ├── test_user_routes.py      # Tests for the API endpoints
  |       |     └── test_integration.py      # Integration tests between components   
  |       └── test_books                     # Test for all books endpoints and all associated models and classes
  ├── functional_test                       
  ├── deployment test
  |          └── conftest.py                 # Common fixtures and test configuration for deployment
  └── conftest.py                            # Common fixtures and test configuration for all tests
  
 
```

## Test Categories

### 1. Unit Tests
- **AuthService Tests**: Tests for password hashing, salt generation, etc.
- **UserModel Tests**: Tests for data validation rules (password complexity, phone format, etc.)
- **UsersRepository Tests**: Tests for database operations with mocked dependencies
- **API Endpoint Tests**: Tests for HTTP endpoints with mocked backend services

### 2. Integration Tests
- Tests that verify the interaction between components
- Tests that validate the complete registration flow from API to repository

## Running Tests

To run all tests:
```bash
pytest
```

To run specific test files:
```bash
pytest tests/test_auth_service.py
pytest tests/test_user_model.py
```

To run tests with verbose output:
```bash
pytest -v
```

To run tests and display print statements:
```bash
pytest -v -s
```

## Test Coverage

To generate a test coverage report:
```bash
pytest --cov=app tests/
```

## Mocking Strategy

- External dependencies are mocked to isolate components
- Database sessions are mocked to avoid actual database operations
- Utility functions like id_generator and renewal are mocked for predictable test results