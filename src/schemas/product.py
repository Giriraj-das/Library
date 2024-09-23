from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: int
    stock_quantity: int


class ProductSchema(ProductBaseSchema):
    id: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdateSchema(ProductCreateSchema):
    pass


class ProductUpdatePartialSchema(ProductCreateSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock_quantity: int | None = None
