from http import HTTPStatus

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
