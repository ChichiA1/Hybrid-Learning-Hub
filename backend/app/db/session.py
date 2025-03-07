from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# create a database connection engine that allows asynchronous operations, returns an Engine object, which is used to
# connect to the database
engine = create_async_engine(DATABASE_URL,
                             future=True,  # compatibilty with the future releases
                             echo=False)  # controls logging of all SQL statements issued to the database

# Create sessionmaker with AsyncSession explicitly passed as class_.
SessionLocal = sessionmaker(
    bind=engine,                # The async engine (AsyncEngine) for binding
    class_=AsyncSession,         # Explicitly specify AsyncSession as the session class
    expire_on_commit=False      # Don't expire objects after committing
)  # type: ignore  # <-- This is where you suppress the Mypy error
