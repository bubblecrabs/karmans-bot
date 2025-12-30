from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.core.config import settings


def get_engine() -> AsyncEngine:
    return create_async_engine(
        url=settings.POSTGRES_DSN,
        echo=settings.DEBUG,
    )


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker[AsyncSession](
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


engine: AsyncEngine = get_engine()
session_maker: async_sessionmaker = get_session_maker(engine=engine)
