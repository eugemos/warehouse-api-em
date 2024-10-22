from http import HTTPStatus

from fastapi import Depends, HTTPException

from app import schemas
from app.core.types import OrderStatus
from app.models import Order
from app.repos import OrderRepo, ProductRepo


class OrderService:
    """Сервис для работы с заказами."""

    def __init__(
        self,
        order_repo: OrderRepo = Depends(OrderRepo),
        product_repo: ProductRepo = Depends(ProductRepo),
    ):
        self._order_repo = order_repo
        self._product_repo = product_repo

    async def create(
        self, data: schemas.CreateOrderRequest
    ) -> schemas.CreateOrderResponse:
        """Создать заказ"""
        errors = []
        items_data = []
        for item in data.items:
            product = await self._product_repo.get(item.product_id)
            if product is None:
                errors.append(
                    dict(product_id=item.product_id,
                         error='этот товар не найден')
                )
                continue

            if product.amount < item.amount:
                errors.append(
                    dict(product_id=item.product_id,
                         error='этого товара не хватает')
                )
                continue

            product.amount -= item.amount
            items_data.append(item.model_dump())

        if errors:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=errors
            )

        order = await self._order_repo.create(
            OrderStatus.PROCESSING, items_data
        )
        return schemas.CreateOrderResponse(
            id=order.id, created_at=order.created_at, status=order.status,
            items=items_data
        )

    async def get_all(self) -> list[Order]:
        """Получить все заказы"""
        return await self._order_repo.get_all()

    async def get_or_error(self, id: int) -> Order:
        """Получить заказ по его id. Если заказ не существует,
        то возбудить исключение.
        """
        return await self._order_repo.get_or_error(id)

    async def update_status(
        self, id: int, new_status: OrderStatus
    ) -> Order:
        """Изменить статус заказа."""
        return await self._order_repo.update(
            id, dict(status=new_status)
        )
