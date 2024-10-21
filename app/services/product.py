from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.models import Product
from app.repos import ProductRepo
from app import schemas


class ProductService:
    def __init__(self, repo: ProductRepo = Depends(ProductRepo)):
        self._repo = repo

    async def create(
        self, data: schemas.CreateProductRequest
    ) -> Product:
        return await self._repo.create(data.model_dump())

    async def get_all(self) -> list[Product]:
        return await self._repo.get_all()

    async def get_or_error(self, id: int) -> Product:
        return await self._repo.get_or_error(id)

    async def update(
        self, id: int, data_for_update: schemas.UpdateProductRequest
    ) -> Product:
        return await self._repo.update(
            id, data_for_update.model_dump(exclude_none=True)
        )

    async def delete(self, id: int) -> None:
        if await self._repo.any_order_exists(id):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Этот товар входит в заказы, его нельзя удалить.'
            )

        await self._repo.delete(id)
