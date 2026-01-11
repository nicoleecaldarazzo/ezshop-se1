from fastapi import APIRouter, Depends, status
from typing import List
from app.controllers.return_controller import ReturnController
from app.models.DTO.return_dto import ReturnDTO
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType
from app.config.config import ROUTES

router = APIRouter(prefix=ROUTES["V1_RETURNS"], tags=["returns"])
controller = ReturnController()

# Returns are managed by all staff roles
auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier]))

@router.post("/", response_model=ReturnDTO, status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def start_return(sale_id: int):
    return await controller.create_return(sale_id)

@router.get("/", response_model=List[ReturnDTO], dependencies=[auth_dep])
async def get_all_returns():
    return await controller.list_returns()

@router.get("/{return_id}", response_model=ReturnDTO, dependencies=[auth_dep])
async def get_return(return_id: int):
    return await controller.get_return(return_id)

@router.delete("/{return_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[auth_dep])
async def delete_return(return_id: int):
    await controller.delete_return(return_id)
    return

@router.get("/sale/{sale_id}", response_model=List[ReturnDTO], dependencies=[auth_dep])
async def get_returns_by_sale(sale_id: int):
    return await controller.list_returns_by_sale(sale_id)

@router.post("/{return_id}/items", status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def add_item(return_id: int, barcode: str, amount: int):
    success = await controller.add_item(return_id, barcode, amount)
    return {"success": success}

@router.delete("/{return_id}/items", status_code=status.HTTP_202_ACCEPTED, dependencies=[auth_dep])
async def remove_item(return_id: int, barcode: str, amount: int):
    success = await controller.remove_item(return_id, barcode, amount)
    return {"success": success}

@router.patch("/{return_id}/close", dependencies=[auth_dep])
async def close_return(return_id: int):
    return await controller.close_return(return_id)

@router.patch("/{return_id}/reimburse", dependencies=[auth_dep])
async def reimburse_return(return_id: int):
    return await controller.reimburse_return(return_id)