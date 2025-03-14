# repository.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.dependencies import get_db_session
from app.database.models.user import UserModel
from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.errors.result_errors.user_errors import UserErrors
from app.shared.core.repository import PostgresRepository
from app.shared.core.result.result import Result
from app.users.domain.user import UserEntity
from app.users.mappers.user_db_map import UserDbMap
from sqlalchemy import select
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

logger = logging.getLogger(__name__)


class UserRepository(PostgresRepository):

    async def get_user_by_id(self, id: str) -> Result[UserEntity]:
        try:
            db_user = (
                await self.db.execute(select(UserModel).where(UserModel.id == id))
            ).scalar_one_or_none()
            if not db_user:
                return Result.fail(UserErrors.not_found(str(id)))
            return Result.ok(UserDbMap.to_domain(db_entity=db_user))
        except Exception as e:
            logger.error(f"Error getting user by id: {e}")
            return Result.fail(DbErrors.unkown_db_error())

    async def get_by_email(self, email: str) -> Result[UserEntity]:
        try:
            db_user = (
                await self.db.execute(select(UserModel).where(UserModel.email == email))
            ).scalar_one_or_none()
            if not db_user:
                return Result.fail(UserErrors.not_found(email))
            return Result.ok(UserDbMap.to_domain(db_entity=db_user))
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return Result.fail(DbErrors.unkown_db_error())

    async def get_by_email_and_password(
        self, email: str, password: str, session: AsyncSession | None = None
    ) -> Result[UserEntity]:
        db = session or self.db
        try:
            print("dbddd", db)
            db_user = (
                await db.execute(select(UserModel).where(UserModel.email == email))
            ).scalar_one_or_none()
            if not db_user:
                return Result.fail(UserErrors.not_found(email))
            if not db_user.verify_password(password):
                return Result.fail(UserErrors.not_found())
            return Result.ok(UserDbMap.to_domain(db_entity=db_user))
        except Exception as e:
            print("eeehahah", e)
            logger.error(f"Error getting user by email and password: {e}")
            return Result.fail(DbErrors.unkown_db_error())

    async def create_user_with_password(
        self, user: UserEntity, password: str, session: AsyncSession | None = None
    ) -> Result[UserEntity]:
        db = session or self.db
        try:
            db_user = UserDbMap.to_db(domain_entity=user)
            db_user.password = password
            db.add(db_user)
            await db.flush()
            if not session:
                await db.commit()
                await db.refresh(db_user)
            print("heyy mannnn", db_user)
            return Result.ok(UserDbMap.to_domain(db_entity=db_user))
        except Exception as e:
            if not session:
                await db.rollback()
            logger.error(f"Error creating user: {e}")
            return Result.fail(DbErrors.unkown_db_error())

    """ def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, name: str, email: str):
        db_user = User(name=name, email=email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, name: str = None, email: str = None):
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        if name is not None:
            db_user.name = name
        if email is not None:
            db_user.email = email
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user"""
