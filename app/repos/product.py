from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Product


class ProductRepo:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def create(self, data: dict) -> Product:
        db_obj = Product(**data)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj

    async def get_all(self) -> list[Product]:
        db_objs = await self._session.scalars(select(Product))
        return db_objs.all()

    async def get(self, id: int) -> Product | None:
        return await self._session.get(Product, id)

    async def get_or_error(self, id: int) -> Product:
        return await self._session.get_one(Product, id)

    async def update(self, id: int, data_for_update: dict) -> Product:
        db_obj = await self.get_or_error(id)
        await self._session.merge(Product(id=db_obj.id, **data_for_update))
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj
