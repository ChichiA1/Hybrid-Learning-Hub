from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database import get_db
from app.models.users import UserModel, UserPublic
from app.db.repositories.users import user_repo

router = APIRouter()


@router.post("/registration/", response_model=UserPublic, name="users:register-user", status_code=HTTP_201_CREATED)
async def register_user(user: UserModel, db: AsyncSession = Depends(get_db)) -> UserPublic:
    return await user_repo.register_user(db=db, user=user)  # type: ignore
