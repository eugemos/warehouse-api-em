from pydantic import BaseModel


from app.core.types import OrderStatus
from .order_item import OrderItem


class BaseOrder(BaseModel):
    items: list[OrderItem]


class FullOrder(BaseOrder):
    id: int
    status: OrderStatus


class CreateOrderRequest(BaseOrder):
    pass


class CreateOrderResponse(FullOrder):
    pass
