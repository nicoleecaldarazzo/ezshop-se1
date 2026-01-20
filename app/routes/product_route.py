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

auth_admin_manager = Depends(authenticate_user([UserType.Administrator, UserType.ShopManager]))
auth_all = Depends(
    authenticate_user([UserType.Administrator, UserType.ShopManager, UserType.Cashier])
)



@router.post(
    "",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def create_product(payload: ProductCreateDTO):
    return await controller.create_product(payload)


@router.get(
    "",
    response_model=List[ProductResponseDTO],
    dependencies=[auth_all],
)
async def list_products():
    return await controller.list_products()


@router.get(
    "/search",
    response_model=List[ProductResponseDTO],
    dependencies=[auth_admin_manager],
)
async def search_products(query: str = Query(..., min_length=1)):  
    from app.models.DTO.product_dto import ProductSearchDTO
    
    search_dto = ProductSearchDTO(description=query)  
    return await controller.search_products(search_dto)

@router.get(
    "/reorder",
    response_model=List[ProductResponseDTO],
    dependencies=[auth_admin_manager],
)
async def get_products_needing_reorder():
    return await controller.get_products_needing_reorder()

@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponseDTO,
    dependencies=[auth_admin_manager],
)
async def get_product_by_barcode(barcode: str = BarcodePattern):
    return await controller.get_product_by_barcode(barcode)




@router.get(
    "/{id}",
    response_model=ProductResponseDTO,
    dependencies=[auth_all],
)
async def get_product(id: int = PositiveId):
    return await controller.get_product(id)


@router.put(
    "/{id}",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def update_product(id: int = PositiveId, payload: ProductUpdateDTO = ...):
    return await controller.update_product(id, payload)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[auth_admin_manager],
)
async def delete_product(id: int = PositiveId):
    await controller.delete_product(id)
    return


@router.patch(
    "/{id}/position",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def update_product_position(id: int = PositiveId, position: str = Query(...)):
    payload = ProductPositionUpdateDTO(position=position)  
    return await controller.update_product_position(id, payload)


@router.patch(
    "/{id}/quantity",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[auth_admin_manager],
)
async def update_product_quantity(id: int = PositiveId, quantity: int = Query(...)):
    return await controller.update_product_quantity(id, quantity)