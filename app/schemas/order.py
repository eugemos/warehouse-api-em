from datetime import datetime

from pydantic import BaseModel, RootModel

from app.core.types import OrderStatus
from .order_item import OrderItem


class BaseOrder(BaseModel):
    items: list[OrderItem]


class FullOrder(BaseOrder):
    id: int
    created_at: datetime
    status: OrderStatus


class CreateOrderRequest(BaseOrder):
    pass


class CreateOrderResponse(FullOrder):
    pass


class ListOrdersResponse(RootModel):
    root: list[FullOrder]


class GetOrderResponse(BaseOrder):
    created_at: datetime
    status: OrderStatus
