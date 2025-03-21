from tokenize import String
import uuid
from sqlalchemy import Column, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from datetime import datetime
import uuid


async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def id(cls) -> Mapped[str]:
        return mapped_column(
            String, primary_key=True, default=lambda: str(uuid.uuid4())
        )

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
