from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product_id: int
    amount: int = Field(gt=0)
