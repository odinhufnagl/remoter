from requests import session
from sqlalchemy import false, insert, select, true, delete
from app.database.models.token import TokenModel
from app.database.models.user import UserModel
from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.errors.result_errors.token_errors import TokenErrors
from app.shared.core.repository import PostgresRepository
from app.shared.core.result.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.core.result.result_error import DefaultResultErrors


class TokenRepository(PostgresRepository):

    async def store_refresh_token(
        self, user_id: str, refresh_token: str, db_session: AsyncSession | None = None
    ) -> Result[None]:
        db = db_session or self.db
        try:
            # Check if a token already exists for the user
            existing_token = await db.execute(
                select(TokenModel).where(TokenModel.user_id == user_id)
            )
            existing_token = existing_token.scalars().first()

            if existing_token:
                # Update the existing token
                existing_token.value = refresh_token
            else:
                # Create a new token
                db_token = TokenModel(user_id=user_id, value=refresh_token)
                db.add(db_token)

            if not db_session:
                await db.commit()
                await db.refresh(existing_token if existing_token else db_token)

            return Result.ok(None)
        except Exception as e:
            await db.rollback()
            return Result.fail(DbErrors.unkown_db_error())

    async def get_and_verify_refresh_token(
        self, user_id: str, refresh_token: str
    ) -> Result[str]:
        try:
            db_token = (
                await self.db.execute(
                    select(TokenModel).where(TokenModel.user_id == user_id)
                )
            ).scalar_one_or_none()
            if not db_token:
                return Result.fail(TokenErrors.token_not_found())
            is_token_verified = db_token.verify_token(refresh_token)
            if not is_token_verified:
                return Result.ok(False)
            return Result.ok(True)
        except Exception as e:
            return Result.fail(DbErrors.unkown_db_error())

    async def delete_refresh_token(self, user_id: str) -> Result[None]:
        try:
            await self.db.execute(
                delete(TokenModel).where(TokenModel.user_id == user_id)
            )
            await self.db.commit()
            return Result.ok(None)
        except Exception as e:
            await self.db.rollback()
            return Result.fail(DbErrors.unkown_db_error())
