import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}\
@localhost/{os.getenv('DB_NAME')}"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession, autoflush=False, expire_on_commit=False, bind=engine.engine
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
