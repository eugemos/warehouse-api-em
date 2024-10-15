from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app import models


class ProductRepo:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def create(self, data: dict) -> models.Product:
        db_obj = models.Product(**data)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj
