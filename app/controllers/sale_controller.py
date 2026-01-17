from fastapi import APIRouter, Depends, status, Response, Path
from typing import List
from app.services.sale_service import SaleService
from app.models.DTO.sale_dto import SaleDTO
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType
from app.config.config import ROUTES

# 1. Define the Controller Class
class SaleController:
    def __init__(self):
        self.service = SaleService()

    async def create_sale(self) -> SaleDTO:
        return await self.service.create_sale()

    async def get_sale(self, sale_id: int) -> SaleDTO:
        return await self.service.get_sale(sale_id)

    async def list_sales(self) -> List[SaleDTO]:
        return await self.service.list_sales()

    async def add_item(self, sale_id: int, barcode: str, amount: int) -> bool:
        return await self.service.add_item(sale_id, barcode, amount)

    async def remove_item(self, sale_id: int, barcode: str, amount: int) -> bool:
        return await self.service.remove_item(sale_id, barcode, amount)

    async def close_sale(self, sale_id: int) -> bool:
        return await self.service.close_sale(sale_id)

    async def pay_sale(self, sale_id: int, cash_amount: float) -> bool:
        return await self.service.pay_sale(sale_id, cash_amount)


router = APIRouter(prefix=ROUTES["V1_SALES"], tags=["sales"])

def get_controller():
    return SaleController()

# Auth Dependency
auth_dep = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier]))

@router.post("/", response_model=SaleDTO, status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def create_sale(
    response: Response,
    controller: SaleController = Depends(get_controller) # <--- FIX: Injected Here
):
    response.status_code = status.HTTP_201_CREATED
    return await controller.create_sale()

@router.get("/", response_model=List[SaleDTO], dependencies=[auth_dep])
async def get_all_sales(
    controller: SaleController = Depends(get_controller)
):
    return await controller.list_sales()

@router.get("/{sale_id}", response_model=SaleDTO, dependencies=[auth_dep])
async def get_sale(
    sale_id: int = Path(..., gt=0),
    controller: SaleController = Depends(get_controller)
):
    return await controller.get_sale(sale_id)

@router.post("/{sale_id}/items", status_code=status.HTTP_201_CREATED, dependencies=[auth_dep])
async def add_item(
    response: Response,
    sale_id: int = Path(..., gt=0),
    barcode: str = "",
    amount: int = 0,
    controller: SaleController = Depends(get_controller)
):
    response.status_code = status.HTTP_201_CREATED
    success = await controller.add_item(sale_id, barcode, amount)
    return {"success": success}

@router.delete("/{sale_id}/items", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def remove_item(
    response: Response,
    sale_id: int = Path(..., gt=0),
    barcode: str = "",
    amount: int = 0,
    controller: SaleController = Depends(get_controller)
):
    response.status_code = status.HTTP_200_OK
    success = await controller.remove_item(sale_id, barcode, amount)
    return {"success": success}

@router.patch("/{sale_id}/close", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def close_sale(
    response: Response,
    sale_id: int = Path(..., gt=0),
    controller: SaleController = Depends(get_controller)
):
    response.status_code = status.HTTP_200_OK
    success = await controller.close_sale(sale_id)
    return {"success": success}

@router.patch("/{sale_id}/pay", status_code=status.HTTP_200_OK, dependencies=[auth_dep])
async def pay_sale(
    response: Response,
    sale_id: int = Path(..., gt=0),
    cash_amount: float = 0.0,
    controller: SaleController = Depends(get_controller)
):
    response.status_code = status.HTTP_200_OK
    success = await controller.pay_sale(sale_id, cash_amount)
    return {"success": success}