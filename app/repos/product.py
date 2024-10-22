from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Product, OrderItem


class ProductRepo:
    """Репозиторий для работы с товарами."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def create(self, data: dict) -> Product:
        """Создать товар"""
        db_obj = Product(**data)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj

    async def get_all(self) -> list[Product]:
        """Получить все товары"""
        db_objs = await self._session.scalars(
            select(Product).order_by(Product.id)
        )
        return db_objs.all()

    async def get_or_error(self, id: int) -> Product:
        """Получить товар по его id. Если товар не существует,
        то возбудить исключение.
        """
        return await self._session.get_one(Product, id)

    async def update(self, id: int, data_for_update: dict) -> Product:
        """Изменить данные товара."""
        db_obj = await self.get_or_error(id)
        await self._session.merge(Product(id=db_obj.id, **data_for_update))
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> None:
        """Удалить товар"""
        db_obj = await self.get_or_error(id)
        await self._session.delete(db_obj)
        await self._session.commit()

    async def any_order_exists(self, id) -> bool:
        """Проверить, существуют ли заказы, куда входит товар"""
        order_count = await self._session.scalar(
            select(func.count('*'))
            .select_from(OrderItem)
            .where(OrderItem.product_id == id)
        )
        return order_count > 0
