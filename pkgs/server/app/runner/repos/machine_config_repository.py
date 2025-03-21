from app.runner.domain.runner_session_entity import MachineConfig
from app.runner.mappers.runner_session_db_map import MachineConfigDbMap
from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.repository import PostgresRepository
from app.shared.core.result.result import Result
from app.shared.core.result.result_error import ResultError
from sqlalchemy.ext.asyncio import AsyncSession


class MachineConfigRepository(PostgresRepository):

    async def save(
        self, entity: MachineConfig, db_session: AsyncSession | None = None
    ) -> Result[None, ResultError]:
        db = db_session or self.db
        try:
            db_entity = MachineConfigDbMap.to_db(entity)
            db.add(db_entity)

            if not db_session:
                await db.commit()
                await db.refresh(db_entity)

            return Result.ok(None)
        except Exception as e:
            if not db_session:
                await db.rollback()
            return Result.fail(DbErrors.unkown_db_error())
