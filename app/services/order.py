from http import HTTPStatus

from fastapi import Depends, HTTPException

from app import schemas
from app.core.types import OrderStatus
from app.repos import ProductRepo


class OrderService:
    def __init__(self, product_repo: ProductRepo = Depends(ProductRepo)):
        self._product_repo = product_repo

    async def create(
        self, data: schemas.CreateOrderRequest
    ) -> schemas.CreateOrderResponse:
        await self._check_create_request(data)
        return schemas.CreateOrderResponse(
            id=0, status=OrderStatus.PROCESSING, items=[]
        )

    async def _check_create_request(
        self, data: schemas.CreateOrderRequest
    ) -> None:
        errors = []
        for item in data.items:
            product = await self._product_repo.get(item.product_id)
            if product is None:
                errors.append(
                    dict(id=item.product_id, error='товар не найден')
                )
                continue

            if product.amount < item.amount:
                errors.append(
                    dict(id=item.product_id, error='товара не хватает')
                )

        print(f'{errors=}')
        if errors:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=errors
            )
