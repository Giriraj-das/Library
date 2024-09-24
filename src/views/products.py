from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from services.product import product_by_id
from models import db_helper, Product
from crud import product as product_crud
from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema

router = APIRouter(prefix=settings.prefix.product, tags=['Products'])


@router.post('', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: ProductCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await product_crud.create_product(session=session, product_data=product_data)


@router.get('', response_model=list[ProductSchema])
async def get_products(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await product_crud.get_products(session=session)


@router.get('/{product_id}', response_model=ProductSchema)
async def get_product(
        product: ProductSchema = Depends(product_by_id),
):
    return product


@router.put("/{product_id}")
async def update_product(
        product_data: ProductUpdateSchema,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await product_crud.update_product(
        session=session,
        product=product,
        product_data=product_data,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await product_crud.delete_product(session=session, product=product)
