from sqlalchemy import Column, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
