from fastapi import APIRouter, Depends
from app.services.sale_service import SaleService
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType

router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])
service = SaleService()

auth_dep = Depends(
    authenticate_user([
        UserType.Administrator,
        UserType.ShopManager,
        UserType.Cashier
    ])
)

@router.post("", dependencies=[auth_dep])
async def create_sale():
    return await service.create_sale()

@router.get("/{sale_id}", dependencies=[auth_dep])
async def get_sale(sale_id: int):
    return await service.get_sale(sale_id)

@router.post("/{sale_id}/items", dependencies=[auth_dep])
async def add_item(sale_id: int, barcode: str, amount: int):
    return await service.add_item(sale_id, barcode, amount)

@router.delete("/{sale_id}/items", dependencies=[auth_dep])
async def remove_item(sale_id: int, barcode: str, amount: int):
    return await service.remove_item(sale_id, barcode, amount)

@router.patch("/{sale_id}/discount", dependencies=[auth_dep])
async def set_discount(sale_id: int, discount: float):
    return await service.set_discount(sale_id, discount)

@router.patch("/{sale_id}/close", dependencies=[auth_dep])
async def close_sale(sale_id: int):
    return await service.close_sale(sale_id)

@router.patch("/{sale_id}/pay", dependencies=[auth_dep])
async def pay_sale(sale_id: int, cash_amount: float):
    return await service.pay_sale(sale_id, cash_amount)

@router.get("/{sale_id}/points", dependencies=[auth_dep])
async def get_points(sale_id: int):
    return await service.compute_points(sale_id)
