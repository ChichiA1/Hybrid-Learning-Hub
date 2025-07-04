import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UserPublic


class TestUserRegistrationIntegration:

    @pytest.mark.asyncio
    async def test_integration_register_flow(self, auth_service, user_repo, test_user):
        """Test the complete user registration flow with dependencies"""
        mock_db = MagicMock(spec=AsyncSession)

        with patch('app.db.repositories.users.id_generator') as mock_id_generator, \
             patch('app.db.repositories.users.renewal') as mock_renewal, \
             patch('app.db.repositories.users.add_update_table') as mock_add_update_table, \
             patch.object(user_repo, 'check_if_user_exist', new_callable=AsyncMock) as mock_check_user_exist:

            mock_check_user_exist.return_value = False
            mock_id_generator.return_value = "test-user-id"
            mock_renewal.return_value = datetime.now() + timedelta(days=365)

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
                "dob": test_user.dob,
                "membership_status": "active",
                "renewal": mock_renewal.return_value
            }
            mock_add_update_table.return_value = mock_user

            with patch('app.db.repositories.users.auth_service', auth_service):
                result = await user_repo.register_user(db=mock_db, user=test_user)

            # ✅ Use object-style access
            assert result.user_id == "test-user-id"
            assert result.email == test_user.email
            assert result.username == test_user.username
            assert result.user_type == test_user.user_type

            mock_add_update_table.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.api.routes.users.user_repo')
    async def test_api_to_repo_integration(self, mock_user_repo, client, test_user):
        """Test the API to repository integration"""

        user_request = {
            "first_name": test_user.first_name,
            "last_name": test_user.last_name,
            "email": test_user.email,
            "username": test_user.username,
            "password": test_user.password,
            "phone": test_user.phone,
            "address": test_user.address,
            "user_type": test_user.user_type.value,
            "dob": test_user.dob.isoformat()
        }

        # Remove password from user_request before passing to UserPublic
        user_response_data = {**user_request}
        user_response_data.pop("password")

        # ✅ Use AsyncMock to match the async nature of the actual register_user
        mock_user_repo.register_user = AsyncMock(return_value=UserPublic(
            user_id="test-user-id",
            password="hashed_password",  # explicitly add it here if needed
            membership_status="active",
            renewal=(datetime.now() + timedelta(days=365)).isoformat(),
            **user_response_data
        ))

        response = client.post("/api/users/registration/", json=user_request)

        # ✅ Ensure endpoint exists and response is correct
        assert response.status_code == 201

        # ✅ Validate repo method call and argument mapping
        mock_user_repo.register_user.assert_called_once()
        call_args = mock_user_repo.register_user.call_args
        user_model = call_args[1]['user']

        assert user_model.first_name == test_user.first_name
        assert user_model.email == test_user.email
        assert user_model.password == test_user.password
