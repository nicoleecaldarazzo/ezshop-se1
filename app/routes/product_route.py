from fastapi import APIRouter, Depends, status, Path, Query
from typing import List

from app.config.config import ROUTES
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType

from app.controllers.product_controller import ProductController
from app.models.DTO.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductResponseDTO,
    ProductPositionUpdateDTO,
)

router = APIRouter(prefix=ROUTES["V1_PRODUCTS"], tags=["Products"])
controller = ProductController()

PositiveId = Path(..., gt=0)
BarcodePattern = Path(..., pattern=r"^\d{12,14}$")

# Auth dependencies
auth_admin_manager = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager]))
auth_all = Depends(
    authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier])
)


# ---- Products CRUD (Base endpoints) ----


@router.post(
    "",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def create_product(payload: ProductCreateDTO):
    """Create a new product type. Requires Administrator or ShopManager role."""
    return await controller.create_product(payload)


@router.get(
    "",
    response_model=List[ProductResponseDTO],
    dependencies=[auth_all],
)
async def list_products():
    """List all product types. Requires Administrator, ShopManager, or Cashier role."""
    return await controller.list_products()


# ---- Product operations (Specific paths - MUST come BEFORE /{id}) ----


@router.get(
    "/search",
    response_model=List[ProductResponseDTO],
    dependencies=[auth_admin_manager],
)
async def search_products(description: str = Query(..., min_length=1)):
    """Search product types by description. Requires Administrator or ShopManager role."""
    from app.models.DTO.product_dto import ProductSearchDTO
    
    search_dto = ProductSearchDTO(description=description)
    return await controller.search_products(search_dto)


@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponseDTO,
    dependencies=[auth_admin_manager],
)
async def get_product_by_barcode(barcode: str = BarcodePattern):
    """Get product by barcode. Requires Administrator or ShopManager role."""
    return await controller.get_product_by_barcode(barcode)


# ---- Products CRUD (Dynamic path parameters - MUST come AFTER specific paths) ----


@router.get(
    "/{id}",
    response_model=ProductResponseDTO,
    dependencies=[auth_all],
)
async def get_product(id: int = PositiveId):
    """Get product type by ID. Requires Administrator, ShopManager, or Cashier role."""
    return await controller.get_product(id)


@router.put(
    "/{id}",
    response_model=ProductResponseDTO,
    dependencies=[auth_admin_manager],
)
async def update_product(id: int = PositiveId, payload: ProductUpdateDTO = ...):
    """Update product type by ID. Requires Administrator or ShopManager role."""
    return await controller.update_product(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[auth_admin_manager],
)
async def delete_product(id: int = PositiveId):
    """Delete product type by ID. Requires Administrator or ShopManager role."""
    await controller.delete_product(id)
    return


@router.patch(
    "/{id}/position",
    response_model=ProductResponseDTO,
    dependencies=[auth_admin_manager],
)
async def update_product_position(id: int = PositiveId, position: str = Query(...)):
    """Assign or clear shelf position. Requires Administrator or ShopManager role."""
    payload = ProductPositionUpdateDTO(position=position)  # Crea il DTO
    return await controller.update_product_position(id, payload)


@router.patch(
    "/{id}/quantity",
    response_model=ProductResponseDTO,
    dependencies=[auth_admin_manager],
)
async def update_product_quantity(id: int = PositiveId, quantity: int = Query(...)):
    """Increase/decrease available quantity. Requires Administrator or ShopManager role."""
    return await controller.update_product_quantity(id, quantity)