from abc import ABC
import logging
from typing import Callable, Self
from venv import logger
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database.dependencies import get_db_session
from app.shared.core.errors.result_errors.db_errors import DbErrors


class PostgresRepository(ABC):
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db
