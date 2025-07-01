import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.users import UserPasswordUpdate, UserPublic
from app.db.repositories.users import UsersRepository


class TestUsersRepository:
    @pytest.mark.asyncio
    @patch('app.db.repositories.users.auth_service')
    @patch('app.db.repositories.users.id_generator')
    @patch('app.db.repositories.users.renewal')
    @patch('app.db.repositories.users.add_update_table')
    @patch('app.db.repositories.users.UsersRepository.check_if_user_exist', new_callable=AsyncMock)
    async def test_register_user(
        self,
        mock_check_if_user_exist,
        mock_add_update_table,
        mock_renewal,
        mock_id_generator,
        mock_auth_service,
        user_repo,
        test_user,
        mock_db
    ):
        """Test registering a user"""
        # Setup mocks
        mock_id_generator.return_value = "test-user-id"
        mock_renewal.return_value = datetime.now() + timedelta(days=365)
        mock_auth_service.create_hashed_password.return_value = UserPasswordUpdate(
            password="hashed_password"
        )
        mock_check_if_user_exist.return_value = None  # Simulate no user conflict

        # Mock the User model creation and to_dict
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "user_id": "test-user-id",
            "first_name": test_user.first_name,
            "last_name": test_user.last_name,
            "email": test_user.email,
            "username": test_user.username,
            "phone": test_user.phone,
            "address": test_user.address,
            "user_type": test_user.user_type,
            "dob": test_user.dob.isoformat()
        }

        # Mock the database operations
        mock_db.add = MagicMock()
        mock_add_update_table.return_value = mock_user

        # Call the function
        result = await user_repo.register_user(db=mock_db, user=test_user)

        # Assertions
        mock_auth_service.create_hashed_password.assert_called_once_with(
            plaintext_password=test_user.password
        )
        mock_id_generator.assert_called_once()
        mock_renewal.assert_called_once()
        mock_db.add.assert_called_once()
        mock_add_update_table.assert_called_once()

        # Validate the result
        assert isinstance(result, UserPublic)
        assert result.user_id == "test-user-id"
        assert result.first_name == test_user.first_name
        assert result.email == test_user.email
        assert result.username == test_user.username
        assert "password" not in result.dict()  # Password should not be in the result

    @pytest.mark.asyncio
    @patch('app.db.repositories.users.auth_service')
    @patch('app.db.repositories.users.id_generator')
    @patch('app.db.repositories.users.renewal')
    @patch('app.db.repositories.users.UsersRepository.check_if_user_exist', new_callable=AsyncMock)
    async def test_register_user_exception(
        mock_check_if_user_exist,
        mock_renewal,
        mock_id_generator,
        mock_auth_service,
        test_user,
        mock_db
    ):
        """Test handling exceptions during user registration"""
        # Setup mocks
        mock_id_generator.return_value = "test-user-id"
        mock_renewal.return_value = datetime.now() + timedelta(days=365)
        mock_auth_service.create_hashed_password.return_value = UserPasswordUpdate(
            password="hashed_password"
        )

        # Simulate a user already exists scenario
        mock_check_if_user_exist.return_value = test_user  # Simulating an existing user

        # Create a real instance of UsersRepository
        user_repo = UsersRepository()

        # Call the function and check for exception
        with pytest.raises(HTTPException) as excinfo:
            await user_repo.register_user(db=mock_db, user=test_user)  # Ensure this call is awaited

        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "email or username is already taken. Register with another one."
