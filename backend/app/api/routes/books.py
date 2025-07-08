from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database import get_db
from app.models.books import BookModel
from app.db.repositories.books import book_repo

router = APIRouter()


@router.post("/add-book/", response_model=BookModel, name="books:add-book", status_code=HTTP_201_CREATED)
async def add_book(book: BookModel, db: AsyncSession = Depends(get_db)) -> BookModel:
    try:
        return await book_repo.add_book(db=db, book=book)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
