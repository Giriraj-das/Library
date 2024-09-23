from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Product
from crud import product as product_crud


async def product_by_id(
    product_id: int = Path,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    product = await product_crud.get_product(session=session, product_id=product_id)
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
