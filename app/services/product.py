from fastapi import Depends

from app import models
from app.repos import ProductRepo
from app import schemas


class ProductService:
    def __init__(self, repo: ProductRepo = Depends(ProductRepo)):
        self._repo = repo
        print(f'{self._repo=}')

    async def create(
        self, data: schemas.CreateProductRequest
    ) -> models.Product:
        return await self._repo.create(data.dict())
