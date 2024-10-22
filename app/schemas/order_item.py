from typing import Annotated

from pydantic import BaseModel, Field

from .product import ProductId

ProductAmount = Annotated[
    int,
    Field(
        gt=0,
        title='Количество',
        description='Количество товара в заказе',
        examples=['10']
    )
]


class OrderItem(BaseModel):
    """Позиция заказа"""
    product_id: ProductId
    amount: ProductAmount
