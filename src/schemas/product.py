from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: int


class ProductCreateSchema(ProductBaseSchema):
    stock_quantity: int


class ProductUpdateSchema(ProductCreateSchema):
    pass


class ProductUpdatePartialSchema(ProductCreateSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock_quantity: int | None = None


class ProductsSchema(ProductBaseSchema):
    id: int


class ProductSchema(ProductCreateSchema):
    id: int
