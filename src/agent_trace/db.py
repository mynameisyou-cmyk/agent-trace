from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from agent_trace.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Separate engine for auth DB (agent_tools)
auth_engine = create_async_engine(settings.auth_database_url, echo=False)
auth_session = async_sessionmaker(auth_engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:  # type: ignore[misc]
    async with async_session() as session:
        yield session
