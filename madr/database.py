from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from madr.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_async_session() -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session
