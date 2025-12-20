from fastapi import APIRouter, Depends, status, Path
from typing import List

from app.config.config import ROUTES
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType

from app.controllers.order_controller import OrderController
from app.models.DTO.order_dto import (
    OrderCreateDTO,
    OrderPayForDTO,
    OrderResponseDTO,
    OrderPaymentDTO,
    OrderArrivalDTO,
)

router = APIRouter(prefix=ROUTES["V1_ORDERS"], tags=["Orders"])
controller = OrderController()

PositiveId = Path(..., gt=0)

# Auth dependency
auth_admin_manager = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager]))


# ---- Orders (CRUD-like operations) ----


@router.post(
    "",
    response_model=OrderResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def create_order(payload: OrderCreateDTO):
    """Issue a new order. Requires Administrator or ShopManager role. 
    The new order is in the ISSUED state."""
    return await controller.create_order(payload)


@router.get(
    "",
    response_model=List[OrderResponseDTO],
    dependencies=[auth_admin_manager],
)
async def list_orders():
    """List all orders. Requires Administrator or ShopManager role."""
    return await controller.list_orders()


# ---- Order operations ----


@router.post(
    "/payfor",
    response_model=OrderResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def create_and_pay_order(payload: OrderPayForDTO):
    """Create and pay an order for a product. Requires Administrator or ShopManager role.
    The new order is in the PAID state. The balance is updated accordingly."""
    return await controller.create_and_pay_order(payload)


@router.patch(
    "/{order_id}/pay",
    response_model=OrderResponseDTO,
    dependencies=[auth_admin_manager],
)
async def pay_order(order_id: int = PositiveId):
    """Pay for an existing ISSUED order. Requires Administrator or ShopManager role.
    The order state is now PAID. The balance is updated accordingly."""
    payload = OrderPaymentDTO()  # DTO vuoto, payment_method sarà None
    return await controller.pay_order(order_id, payload)


@router.patch(
    "/{order_id}/arrival",
    response_model=OrderResponseDTO,
    dependencies=[auth_admin_manager],
)
async def record_order_arrival(order_id: int = PositiveId):
    """Record the arrival of an order. Requires Administrator or ShopManager role."""
    payload = OrderArrivalDTO()  # DTO vuoto, notes sarà None
    return await controller.record_order_arrival(order_id, payload)