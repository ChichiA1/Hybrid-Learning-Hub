from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.db.base import Base
from app.orm_model.user import User
from app.core.config import DATABASE_URL
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
print(DATABASE_URL)
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Read the DATABASE_URL from the environment variables
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://${USER}:${PASSWORD}@${HOST}/${DBNAME}")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

def run_migrations_offline():
    try:
        """Run migrations in 'offline' mode."""
        context.configure(
            url=DATABASE_URL,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        print(f"An error occurred during offline migration: {e}")

async def run_migrations_online():
    try:
        """Run migrations in 'online' mode."""
        connectable = create_async_engine(
            DATABASE_URL,
            poolclass=pool.NullPool,
        )

        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"An error occurred during online migration: {e}")

def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
