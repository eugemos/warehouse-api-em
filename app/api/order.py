# from http import HTTPStatus

from fastapi import APIRouter, Depends

from app import models
from app import schemas
from app.services import OrderService

router = APIRouter()


@router.post(
    '',
    response_model=schemas.CreateOrderResponse
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
