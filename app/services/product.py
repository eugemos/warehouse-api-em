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
        return await self._repo.create(data.dict())

    async def get_all(self) -> list[Product]:
        return await self._repo.get_all()

    async def get_or_error(self, id_: int) -> Product:
        obj = await self._repo.get(id_)
        if obj is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Объект не найден!'
            )

        return obj
