from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    url=settings.POSTGRES_DSN,
    echo=settings.DEBUG,
)

session_maker: async_sessionmaker = async_sessionmaker[AsyncSession](
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
