from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category, Product


async def get_categories(db: AsyncSession):
    result = await db.execute(
        select(Category).order_by(Category.id)
    )
    return result.scalars().all()


async def get_products(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(Product).where(
            Product.category_id == category_id
        ).order_by(Product.id)
    )
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int):
    return await db.get(Product, product_id)
