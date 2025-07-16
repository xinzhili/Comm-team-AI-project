from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from utils.config import get_config
from utils.logger import logger

async_session: Optional[async_sessionmaker[AsyncSession]] = None


def init_orm() -> None:
    global async_session
    logger.info('Initializing ORM...')

    config = get_config()
    db_url = config.get('database_url', '')

    if not db_url:
        raise ValueError("DATABASE_URL is not configured")

    engine = create_async_engine(
        url=db_url,
        pool_size=10,
        max_overflow=20,
        pool_timeout=60,
    )

    async_session = async_sessionmaker(
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        bind=engine
    )


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if async_session is None:
        raise RuntimeError('Call init_qa_orm_() first to initialize database')

    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            logger.exception("Database transaction rolled back due to error")
            raise
