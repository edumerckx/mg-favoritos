from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mg_favoritos.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
