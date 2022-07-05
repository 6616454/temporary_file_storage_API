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

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)


def get_session_sync() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
