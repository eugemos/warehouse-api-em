from http import HTTPStatus

from fastapi import APIRouter, Body, Depends

from app import models
from app import schemas
from app.core.types import OrderStatus
from app.services import OrderService

router = APIRouter()


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=schemas.CreateOrderResponse,
)
async def create_order(
    request_body: schemas.CreateOrderRequest,
    order_service: OrderService = Depends(OrderService),
):
    return await order_service.create(request_body)


@router.get(
    '',
    response_model=schemas.ListOrdersResponse,
)
async def list_orders(
    order_service: OrderService = Depends(OrderService),
) -> list[models.Order]:
    return await order_service.get_all()


@router.get(
    '/{id}',
    response_model=schemas.GetOrderResponse,
)
async def get_order(
    id: int,
    order_service: OrderService = Depends(OrderService),
) -> models.Order:
    return await order_service.get_or_error(id)


@router.patch(
    '/{id}/status',
    response_model=schemas.GetOrderResponse,
)
async def update_order_state(
    id: int,
    new_status: OrderStatus = Body(),
    order_service: OrderService = Depends(OrderService),
) -> models.Order:
    return await order_service.update_status(id, new_status)
