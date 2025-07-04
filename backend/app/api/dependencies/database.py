from app.db.session import SessionLocal


async def get_db():
    # `async with` takes care of closing the session automatically once it is done
    async with SessionLocal() as session:
        yield session


async def add_update_table(db, data):
    await db.commit()  # Commit the transaction
    # Refresh the object to get the latest state from the database
    await db.refresh(data)
    return data
