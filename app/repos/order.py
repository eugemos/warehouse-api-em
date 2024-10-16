from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.types import OrderStatus
from app.core.db import get_async_session
from app.models import Order, OrderItem


class OrderRepo:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def create(
        self, order_status: OrderStatus, items_data: list[dict]
    ) -> Order:
        order = Order(status=order_status)
        self._session.add(order)
        await self._session.flush()
        for item_data in items_data:
            item_data['order_id'] = order.id

        await self._session.execute(insert(OrderItem), items_data)
        await self._session.commit()
        await self._session.refresh(order)
        return order

    async def get_all(self) -> list[Order]:
        db_objs = await self._session.scalars(select(Order))
        return db_objs.unique().all()
