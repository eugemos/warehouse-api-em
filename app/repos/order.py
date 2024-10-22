from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.types import OrderStatus
from app.core.db import get_async_session
from app.models import Order, OrderItem


class OrderRepo:
    """Репозиторий для работы с заказами."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def create(
        self, order_status: OrderStatus, items_data: list[dict]
    ) -> Order:
        """Создать заказ"""
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
        """Получить все заказы"""
        db_objs = await self._session.scalars(select(Order))
        return db_objs.unique().all()

    async def get_or_error(self, id: int) -> Order:
        """Получить заказ по его id. Если заказ не существует,
        то возбудить исключение.
        """
        return await self._session.get_one(Order, id)

    async def update(self, id: int, data_for_update: dict) -> Order:
        """Изменить данные заказа."""
        db_obj = await self.get_or_error(id)
        await self._session.merge(Order(id=db_obj.id, **data_for_update))
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj
