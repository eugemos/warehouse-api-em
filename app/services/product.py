from fastapi import Depends

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

    async def get_or_error(self, id: int) -> Product:
        return await self._repo.get_or_error(id)
