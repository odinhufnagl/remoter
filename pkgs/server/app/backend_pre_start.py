import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.database.database import engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init(db_engine: AsyncEngine) -> None:
    try:
        async with AsyncSession(db_engine) as session:
            # Use await to execute the query and check that the DB is responsive
            await session.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
