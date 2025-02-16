from app.db.session import SessionLocal

async def get_db():
    # `async with` takes care of closing the session automatically once it is done
    async with SessionLocal() as session:
        yield session