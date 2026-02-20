from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

SessionLocal: async_sessionmaker[AsyncSession] | None = None


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global SessionLocal
    if SessionLocal is None:
        settings = get_settings()
        engine = create_async_engine(settings.database_url, future=True, pool_pre_ping=True)
        SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    return SessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = _get_session_factory()
    async with session_factory() as session:
        yield session
