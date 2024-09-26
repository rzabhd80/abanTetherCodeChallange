import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.models.user import User
from core.models.order import Order
from core.models.base import Base


class DatabaseConfig:
    async_session_local = None

    @classmethod
    def init_database(cls):
        database_url = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}\
            @localhost/{os.getenv('DB_NAME')}"

        engine = create_async_engine(
            database_url,
            pool_size=20,
            max_overflow=0,
            pool_timeout=30,
            pool_recycle=1800,
        )

        cls.async_session_local = sessionmaker(
            class_=AsyncSession, autoflush=False, expire_on_commit=False, bind=engine.engine
        )

    @classmethod
    async def get_db(cls):
        async with cls.async_session_local() as session:
            yield session
