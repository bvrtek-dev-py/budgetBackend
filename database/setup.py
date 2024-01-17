from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from backend.config.database import DATABASE_URL

SessionLocal = async_sessionmaker[AsyncSession]


def async_engine_factory() -> AsyncEngine:
    return create_async_engine(url=DATABASE_URL, pool_size=50, max_overflow=100)


@asynccontextmanager
async def _get_session_context(
    async_engine: Annotated[AsyncEngine, Depends(async_engine_factory)]
) -> AsyncIterator[async_scoped_session[AsyncSession]]:
    session_local = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False
    )
    session = async_scoped_session(session_local, scopefunc=current_task)

    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_session(
    session_context: Annotated[AsyncSession, Depends(_get_session_context)]
) -> AsyncGenerator[AsyncSession, None]:
    async with session_context as session:
        yield session
