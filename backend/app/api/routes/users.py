from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database import get_db
from app.models.users import UserModel, UserPublic
from app.db.repositories.users import user_repo

router = APIRouter()


@router.post("/registration/", response_model=UserPublic, name="users:register-user",
             summary="Register new users", status_code=HTTP_201_CREATED)
async def register_user(user: UserModel, db: AsyncSession = Depends(get_db)) -> UserPublic:
    """
    Checks if user already exists. If user does not exist, it hashes users password and stores user info to the database

    - **user** Mandatory request parameter from client
    - **db** Database async session throught dependency injection
    - **UserPublic** Mandatory response output to client
    """
    try:
        return await user_repo.register_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
