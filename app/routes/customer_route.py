from fastapi import APIRouter, Depends, status, Path, Query
from typing import List

from app.config.config import ROUTES
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType

from app.controllers.customer_controller import CustomerController
from app.models.DTO.customer_dto import (
    CustomerCreateDTO, CustomerUpdateDTO, CustomerResponseDTO,
    LoyaltyCardCreateDTO, LoyaltyCardPointsUpdateDTO, LoyaltyCardDTO
)

router = APIRouter(prefix=ROUTES["V1_CUSTOMERS"], tags=["Customers"])
controller = CustomerController()

PositiveId = Path(..., gt=0)
CardId = Path(..., pattern=r"^\d{10}$")

auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier]))


@router.post(
    "",
    response_model=CustomerResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_dep],
)
async def create_customer(payload: CustomerCreateDTO):
    return await controller.create_customer(payload)


@router.get(
    "",
    response_model=List[CustomerResponseDTO],
    dependencies=[auth_dep],
)
async def list_customers():
    return await controller.list_customers()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponseDTO,
    dependencies=[auth_dep],
)
async def get_customer(customer_id: int = PositiveId):
    return await controller.get_customer(customer_id)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponseDTO,
    dependencies=[auth_dep],
)
async def update_customer(customer_id: int = PositiveId, payload: CustomerUpdateDTO = ...):
    return await controller.update_customer(customer_id, payload)


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[auth_dep],
)
async def delete_customer(customer_id: int = PositiveId):
    await controller.delete_customer(customer_id)
    return


# Swagger: POST /customers/cards
@router.post(
    "/cards",
    response_model=LoyaltyCardDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_dep],
)
async def create_card(payload: LoyaltyCardCreateDTO):
    return await controller.create_card(payload)


# Swagger: PATCH /customers/{customer_id}/attach-card/{card_id}
@router.patch(
    "/{customer_id}/attach-card/{card_id}",
    response_model=CustomerResponseDTO,
    dependencies=[auth_dep],
)
async def attach_card(customer_id: int = PositiveId, card_id: str = CardId):
    return await controller.attach_card(customer_id, card_id)


# Swagger: PATCH /customers/cards/{card_id}
@router.patch("/cards/{card_id}", response_model=LoyaltyCardDTO, dependencies=[auth_dep])
async def update_card_points(card_id: str, points: int = Query(..., ge=0)):
    card = await controller.update_card_points(card_id, points)
    if not card:
        raise NotFoundError("Card not found")
    return card
