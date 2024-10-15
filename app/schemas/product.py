from pydantic import BaseModel, Field

from app.core.constants import MAX_PRODUCT_NAME_LENGTH


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=MAX_PRODUCT_NAME_LENGTH)
    description: str | None = None
    price: int = Field(ge=0)
    amount: int = Field(ge=0)


class CreateProductResponse(CreateProductRequest):
    id: int
