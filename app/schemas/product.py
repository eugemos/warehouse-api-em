from typing import Annotated

from pydantic import BaseModel, Field, RootModel

from app.core.constants import MAX_PRODUCT_NAME_LENGTH

ProductName = Annotated[
    str, Field(min_length=1, max_length=MAX_PRODUCT_NAME_LENGTH)
]
ProductDescription = str | None
ProductPrice = Annotated[int, Field(ge=0)]
ProductAmount = Annotated[int, Field(ge=0)]


class BaseProduct(BaseModel):
    name: ProductName
    description: ProductDescription = None
    price: ProductPrice
    amount: ProductAmount


class FullProduct(BaseProduct):
    id: int


class CreateProductRequest(BaseProduct):
    pass


class CreateProductResponse(FullProduct):
    pass


class ListProductsResponse(RootModel):
    root: list[FullProduct]


class GetProductResponse(BaseProduct):
    pass


class UpdateProductRequest(BaseModel):
    name: ProductName | None = None
    description: ProductDescription = None
    price: ProductPrice | None = None
    amount: ProductAmount | None = None


class UpdateProductResponse(BaseProduct):
    pass
