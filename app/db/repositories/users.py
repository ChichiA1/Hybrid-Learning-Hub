from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm_model.user import User
from app.models.users import UserModel, Membership_status
from app.services.authentication import auth_service
from sqlalchemy.exc import SQLAlchemyError
from app.utils.util import renewal, id_generator
import logging

# Setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UsersRepository:
    """"
    All database actions associated with the Users resource
    """
    # The register_user function to create a new user and commit to the DB
    async def register_user(db: AsyncSession, user: UserModel):
        try:
            # Get hashed password and salt
            salt_and_hashed_password = auth_service.create_salt_and_hashed_password(
                plaintext_password=user.password
            )
            print(user)
            # Convert Pydantic model to dictionary
            user_data = user.dict()
            print(user_data)
            # Update with hashed password and salt
            user_data.update({
                'user_id': id_generator(),
                'password': salt_and_hashed_password.password,  # Store hashed password
                'salt': salt_and_hashed_password.salt,
                'membership_status': Membership_status.active,
                'renewal': renewal()
            })
            logger.debug(f"user_data: {user_data}")

            # Create new User instance
            db_user = User(**user_data)
            # This stages db_user object to be added to the database, not asynchronous, local opertation that happens
            # in memory
            db.add(db_user)
            await db.commit()  # Commit the transaction
            # Refresh the object to get the latest state from the database
            await db.refresh(db_user)
            return db_user.to_dict()
        except SQLAlchemyError as e:
            # If an error occurs during user creation, log and handle the exception
            await db.rollback()
            logger.error(f"Error creating user in the database: {e}")
            raise  # Re-raise the exception so the caller knows something went wrong
        except Exception as e:
            # Catch any unexpected errors
            logger.error(f"Unexpected error while creating user: {e}")
            raise  # Re-raise to propagate the error
