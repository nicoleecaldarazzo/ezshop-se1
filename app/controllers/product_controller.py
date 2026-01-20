from typing import List

from app.services.product_service import ProductService
from app.models.DTO.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductResponseDTO,
    ProductPositionUpdateDTO,
    ProductSearchDTO,
)


class ProductController:
    def __init__(self):
        self.service = ProductService()


    async def create_product(self, product_dto: ProductCreateDTO) -> ProductResponseDTO:
        return await self.service.create_product(product_dto)

    async def get_product(self, product_id: int) -> ProductResponseDTO:
        return await self.service.get_product(product_id)

    async def list_products(self) -> List[ProductResponseDTO]:
        return await self.service.list_products()

    async def update_product(
        self, product_id: int, product_dto: ProductUpdateDTO
    ) -> ProductResponseDTO:
        return await self.service.update_product(product_id, product_dto)

    async def delete_product(self, product_id: int) -> bool:
        return await self.service.delete_product(product_id)



    async def get_product_by_barcode(self, barcode: str) -> ProductResponseDTO:
        return await self.service.get_product_by_barcode(barcode)

    async def search_products(self, search_dto: ProductSearchDTO) -> List[ProductResponseDTO]:
        return await self.service.search_products(search_dto)

    async def update_product_position(
        self, product_id: int, position_dto: ProductPositionUpdateDTO
    ) -> ProductResponseDTO:
        return await self.service.update_product_position(product_id, position_dto)

    async def update_product_quantity(
        self, product_id: int, quantity_delta: int
    ) -> ProductResponseDTO:
        return await self.service.update_product_quantity(product_id, quantity_delta)
    
    async def get_products_needing_reorder(self) -> List[ProductResponseDTO]:
        return await self.service.get_products_needing_reorder()