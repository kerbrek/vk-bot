import asyncio

from sqlalchemy import insert

from bot import database, init_db, models

categories = ["Хлеб", "Булочки", "Пироженые"]
products = ["Хлеб", "Булочка", "Пироженое"]
description = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
    "eiusmod tempor incididunt ut labore et dolore magna aliqua."
)


async def insert_data():
    await init_db.drop_tables()
    await init_db.create_tables()

    async with database.engine.begin() as conn:
        for i, c, p in zip(range(1, 4), categories, products):
            await conn.execute(
                insert(models.Category).values(name=f"{c}")
            )
            for n in range(1, 4):
                await conn.execute(
                    insert(models.Product).values(
                        name=f"{p} #{n}",
                        description=f"{description}",
                        category_id=i,
                    )
                )


if __name__ == "__main__":
    asyncio.run(insert_data())
