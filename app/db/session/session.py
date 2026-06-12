from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.config.config import db_settings

engine = create_async_engine(db_settings.DATABASE_URL, echo=True)


async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()