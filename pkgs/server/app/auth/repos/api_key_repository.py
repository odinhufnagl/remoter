from requests import session
from sqlalchemy import false, insert, select, true, delete
from app.database.models.api_key import ApiKeyModel
from app.shared.core.errors.result_errors.api_key_errors import (
    ApiKeyErrors,
)
from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.repository import PostgresRepository
from app.shared.core.result.result import Result
from sqlalchemy.ext.asyncio import AsyncSession


class ApiKeyRepository(PostgresRepository):

    async def get_user_id_by_api_key_and_public(
        self, api_key: str, public_key: str
    ) -> Result[str]:
        try:
            candidates = (
                (
                    await self.db.execute(
                        select(ApiKeyModel).where(ApiKeyModel.public_key == public_key)
                    )
                )
                .scalars()
                .all()
            )
            for candidate in candidates:
                if candidate.verify_api_key(api_key):
                    return Result.ok(candidate.user_id)

            return Result.fail(ApiKeyErrors.key_not_found())

        except Exception as e:
            return Result.fail(DbErrors.unkown_db_error())

    async def create_api_key(
        self,
        user_id: str,
        api_key: str,
        public_key: str,
        db_session: AsyncSession | None = None,
    ) -> Result[None]:
        db = db_session or self.db
        try:
            db_api_key = ApiKeyModel(
                user_id=user_id, value=api_key, public_key=public_key
            )
            db.add(db_api_key)

            if not db_session:
                await db.commit()
                await db.refresh(db_api_key)

            return Result.ok(None)
        except Exception as e:
            print("eeee", e)
            await db.rollback()
            return Result.fail(DbErrors.unkown_db_error())
