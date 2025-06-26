from fastapi import HTTPException
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.orm_model.user import User
from app.models.users import UserModel, Membership_status, UserPublic
from app.services.authentication import auth_service
from app.utils.util import renewal, id_generator
from app.api.dependencies.database import add_update_table
import logging

# Setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UsersRepository:

    """"
    All database actions associated with the Users resource
    """

    async def check_if_user_exist(self, db: AsyncSession, email: str, username: str) -> Union[str, None]:
        try:
            # Check if the email or username already exists
            stmt = select(User).filter((User.email == email) | (User.username == username))
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Error checking if user exist in db: {e}")
            raise  # Re-raise the exception so the caller knows something went wrong
        return existing_user

    # The register_user function to create a new user and commit to the DB
    async def register_user(self, db: AsyncSession, user: UserModel) -> UserPublic:
        try:
            if await self.check_if_user_exist(db, user.email, user.username):
                print(self.check_if_user_exist(db, user.email, user.username))
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="email or username is already taken. Register with another one."
                )
            # Get hashed password
            hashed_password = auth_service.create_hashed_password(
                plaintext_password=user.password
            )
            print(user)
            # Convert Pydantic model to dictionary
            user_data = user.dict()
            print(user_data)
            # Update with hashed password and salt
            user_data.update({
                'user_id': id_generator(),
                'password': hashed_password.password,  # Store hashed password
                'membership_status': Membership_status.active,
                'renewal': renewal()
            })
            logger.debug(f"user_data: {user_data}")

            # Create new User instance
            db_user = User(**user_data)
            # This stages db_user object to be added to the database, not asynchronous, local opertation that happens
            # in memory
            db.add(db_user)
            db_user = await add_update_table(db, db_user)
            # Exclude password from the response
            user_dict = db_user.to_dict()
            user_dict.pop('password', None)  # Remove the password from the dictionary

            return UserPublic(**user_dict)

        except (SQLAlchemyError, Exception) as e:
            # Handle any SQLAlchemy-related or unexpected errors
            logger.error(f"Error creating user in the database: {e}")
            raise  # Re-raise the exception so the caller knows something went wrong


user_repo = UsersRepository()
