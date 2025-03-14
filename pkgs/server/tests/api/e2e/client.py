from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
import asyncio
from app.database.database import BaseModel
from app.database.dependencies import get_db_session
from app.main import app

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


asyncio.run(init_db())


# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
async def session():
    connection = await engine.connect()
    transaction = await connection.begin()
    session = async_session(bind=connection)
    nested = await connection.begin_nested()

    @sqlalchemy.event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(sync_session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db
    yield TestClient(app, raise_server_exceptions=False)
    del app.dependency_overrides[get_db_session]
