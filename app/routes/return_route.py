from fastapi import APIRouter, Depends, status, Response, Path, Query, HTTPException
from typing import List
from app.controllers.return_controller import ReturnController
from app.models.DTO.return_dto import ReturnDTO
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType
from app.config.config import ROUTES

# 1. Setup Router
router = APIRouter(prefix=ROUTES["V1_RETURNS"], tags=["returns"])

# 2. Dependency Helper
def get_controller():
    return ReturnController()

# 3. Auth Dependencies
# General auth for reading/creating returns (includes Cashier)
auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier]))

reimburse_auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager]))

@router.post("/", response_model=ReturnDTO, status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def start_return(
    response: Response,
    sale_id: int = Query(..., gt=0),
    controller: ReturnController = Depends(get_controller) 
):
    response.status_code = status.HTTP_201_CREATED
    return await controller.create_return(sale_id)

@router.get("/", response_model=List[ReturnDTO], dependencies=[auth_dep])
async def get_all_returns(
    controller: ReturnController = Depends(get_controller)
):
    return await controller.list_returns()

@router.get("/{return_id}", response_model=ReturnDTO, dependencies=[auth_dep])
async def get_return(
    return_id: int = Path(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    return await controller.get_return(return_id)

@router.delete("/{return_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[auth_dep])
async def delete_return(
    response: Response,
    return_id: int = Path(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    await controller.delete_return(return_id)
    response.status_code = status.HTTP_204_NO_CONTENT
    return 

@router.get("/sale/{sale_id}", response_model=List[ReturnDTO], dependencies=[auth_dep])
async def get_returns_by_sale(
    sale_id: int = Path(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    return await controller.list_returns_by_sale(sale_id)

@router.post("/{return_id}/items", status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def add_item(
    response: Response, 
    return_id: int = Path(..., gt=0), 
    barcode: str = Query(...), 
    amount: int = Query(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    response.status_code = status.HTTP_201_CREATED
    success = await controller.add_item(return_id, barcode, amount)
    return {"success": success}

@router.delete("/{return_id}/items", status_code=status.HTTP_202_ACCEPTED, dependencies=[auth_dep])
async def remove_item(
    response: Response,
    return_id: int = Path(..., gt=0),
    barcode: str = Query(...), 
    amount: int = Query(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    success = await controller.remove_item(return_id, barcode, amount)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"success": success}

@router.patch("/{return_id}/close", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def close_return(
    response: Response,
    return_id: int = Path(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    response.status_code = status.HTTP_200_OK
    return await controller.close_return(return_id)

@router.patch("/{return_id}/reimburse", status_code=status.HTTP_200_OK, dependencies=[reimburse_auth_dep])
async def reimburse_return(
    response: Response,
    return_id: int = Path(..., gt=0),
    controller: ReturnController = Depends(get_controller)
):
    response.status_code = status.HTTP_200_OK
    return await controller.reimburse_return(return_id)