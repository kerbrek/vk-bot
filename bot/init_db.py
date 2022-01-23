import asyncio

from . import database, models


async def create_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def drop_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
