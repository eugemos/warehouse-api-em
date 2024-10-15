from pydantic import BaseModel, Field

from app.core.constants import MAX_PRODUCT_NAME_LENGTH


class BaseProduct(BaseModel):
    name: str = Field(min_length=1, max_length=MAX_PRODUCT_NAME_LENGTH)
    description: str | None = None
    price: int = Field(ge=0)
    amount: int = Field(ge=0)


class CreateProductRequest(BaseProduct):
    pass


class CreateProductResponse(BaseProduct):
    id: int


class GetProductResponse(BaseProduct):
    pass
