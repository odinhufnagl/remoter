from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database.database import async_session
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
