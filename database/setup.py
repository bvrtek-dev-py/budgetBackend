from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from budgetBackend.config.database import DATABASE_URL

SessionLocal = async_sessionmaker[AsyncSession]


async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL, pool_size=20, max_overflow=30
)

session_class: SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_class.begin() as session:
        try:
            yield session

        except:
            await session.rollback()

        finally:
            await session.close()
