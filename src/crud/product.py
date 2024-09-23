from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product
from schemas.product import ProductCreateSchema, ProductUpdateSchema, ProductUpdatePartialSchema


async def create_product(session: AsyncSession, product_data: ProductCreateSchema) -> Product:
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    return product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def update_product(
        session: AsyncSession,
        product: Product,
        product_data: ProductUpdateSchema | ProductUpdatePartialSchema,
        partial: bool = False,
) -> Product:
    for name, value in product_data.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()
