from fastapi import APIRouter, Depends, status, Response, Path, Query
from typing import List
from app.services.sale_service import SaleService
from app.models.DTO.sale_dto import SaleDTO
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType
from app.config.config import ROUTES

router = APIRouter(prefix=ROUTES["V1_SALES"], tags=["sales"])

def get_controller():
    return SaleService()

auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier]))

@router.post("/", response_model=SaleDTO, status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def create_sale(service: SaleService = Depends(get_controller)):
    return await service.create_sale()

@router.get("/{sale_id}", response_model=SaleDTO, dependencies=[auth_dep])
async def get_sale(sale_id: int = Path(..., gt=0), service: SaleService = Depends(get_controller)):
    return await service.get_sale(sale_id)

@router.delete("/{sale_id}/items", status_code=status.HTTP_202_ACCEPTED, dependencies=[auth_dep])
async def remove_item(
    sale_id: int = Path(..., gt=0),
    barcode: str = Query(...),
    amount: int = Query(...),
    service: SaleService = Depends(get_controller)
):
    await service.remove_item(sale_id, barcode, amount)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.patch("/{sale_id}/close", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def close_sale(
    sale_id: int = Path(..., gt=0),
    service: SaleService = Depends(get_controller)
):
    await service.close_sale(sale_id)
    return Response(status_code=status.HTTP_200_OK)

@router.patch("/{sale_id}/pay", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def pay_sale(
    sale_id: int = Path(..., gt=0),
    cash_amount: float = Query(...),
    service: SaleService = Depends(get_controller)
):
    change = await service.pay_sale(sale_id, cash_amount)
    return {"change": change}