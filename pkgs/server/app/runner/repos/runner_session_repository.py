from requests import session
from sqlalchemy import false, insert, select, true, delete
from app.database.models.runner_session import RunnerSessionModel
from app.database.models.token import TokenModel
from app.database.models.user import UserModel
from app.runner.domain.runner_session_entity import RunnerSessionEntity
from app.runner.mappers.runner_session_db_map import RunnerSessionDbMap
from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.errors.result_errors.token_errors import TokenErrors
from app.shared.core.repository import PostgresRepository
from app.shared.core.result.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.core.result.result_error import DefaultResultErrors, ResultError


class RunnerSessionRepository(PostgresRepository):

    async def create(
        self,
        user_id: str,
        machine_config_id: str,
        machine_session_id,
        db_session: AsyncSession | None = None,
    ):
        db = db_session or self.db
        try:
            db_runner_session = RunnerSessionModel(
                machine_config_id=machine_config_id,
                machine_session_id=machine_session_id,
                user_id=user_id,
            )
            db.add(db_runner_session)

            if not db_session:
                await db.commit()
                await db.refresh(db_runner_session)

            return Result.ok(RunnerSessionDbMap.to_domain(db_runner_session))
        except Exception as e:
            if not db_session:
                await db.rollback()
            return Result.fail(DbErrors.unkown_db_error())

    async def get_by_user_id(
        self,
        user_id: str,
        db_session: AsyncSession | None = None,
    ) -> Result[list[RunnerSessionEntity], ResultError]:
        db = db_session or self.db
        try:
            db_runner_sessions = list(
                (
                    await db.execute(
                        select(RunnerSessionModel).where(
                            RunnerSessionModel.user_id == user_id
                        )
                    )
                )
                .scalars()
                .all()
            )
            return Result.ok(RunnerSessionDbMap.to_domain_bulk(db_runner_sessions))
        except Exception as e:

            return Result.fail(DbErrors.unkown_db_error())
