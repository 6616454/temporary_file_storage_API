from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_async_engine(
    settings.database_url,
)

async_session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
