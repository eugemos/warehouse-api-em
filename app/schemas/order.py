from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, RootModel

from app.core.types import OrderStatus
from .order_item import OrderItem


OrderId = Annotated[
    int,
    Field(
        title='Идентификатор',
        description='Идентификатор заказа',
        examples=[1]
    ),
]

OredrCreationTime = Annotated[
    datetime,
    Field(
        title='Время создания',
        description='Время создания заказа',
    )
]


class BaseOrder(BaseModel):
    """Базовая информация о заказе"""

    items: list[OrderItem]


class FullOrder(BaseOrder):
    """Полная информация о заказе"""

    id: OrderId
    created_at: OredrCreationTime
    status: OrderStatus


class CreateOrderRequest(BaseOrder):
    """Запрос на создание заказа"""

    pass


class CreateOrderResponse(FullOrder):
    """Ответ на запрос на создание заказа"""

    pass


class ListOrdersResponse(RootModel):
    """Ответ на запрос о получении списка заказов"""

    root: list[FullOrder]


class GetOrderResponse(BaseOrder):
    """Ответ на запрос о получении информации о заказе"""

    created_at: OredrCreationTime
    status: OrderStatus


class UpdateOrderStatusResponse(GetOrderResponse):
    """Ответ на запрос на изменение состояния заказа"""

    pass
