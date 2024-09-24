from datetime import datetime

from pydantic import BaseModel


class ProductQuantitySchema(BaseModel):
    id: int
    quantity: int | None = None


class ProductNameSchema(BaseModel):
    id: int
    name: str


class OrderItemSchema(BaseModel):
    product: ProductNameSchema
    quantity: int


class OrderBaseSchema(BaseModel):
    status: str


class OrderCreateSchema(OrderBaseSchema):
    status: str | None = None
    products_details: list[ProductQuantitySchema]


class OrderUpdatePartialSchema(OrderBaseSchema):
    pass


class OrderSchema(OrderBaseSchema):
    id: int
    created_at: datetime


class OrderInfoNameSchema(OrderSchema):
    products_details: list[OrderItemSchema]
