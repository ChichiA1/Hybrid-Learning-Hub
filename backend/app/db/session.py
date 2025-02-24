from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# create a database connection engine that allows asynchronous operations, returns an Engine object, which is used to
# connect to the database
engine = create_async_engine(DATABASE_URL,
                             future=True,# compatibilty with the future releases
                             echo=True)# controls logging of all SQL statements issued to the database

# create factory function that creates a new session when called
SessionLocal = sessionmaker(bind=engine, # responsible for managing the connection to the database
                            class_=AsyncSession, # allowing you to perform database operations in an asynchronous manner
                            expire_on_commit=False) # do not discard the data object stored in the session after commit
