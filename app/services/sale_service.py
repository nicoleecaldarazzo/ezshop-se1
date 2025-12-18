from app.repositories.sale_repository import SaleRepository
from app.models.sale_status import SaleStatus
from app.models.DTO.boolean_response_dto import BooleanResponseDTO
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.conflict_error import ConflictError

class SaleService:
    def __init__(self):
        self.repo = SaleRepository()

    async def create_sale(self):
        return await self.repo.create_sale()

    async def get_sale(self, sale_id: int):
        sale = await self.repo.get_sale(sale_id)
        if not sale:
            raise NotFoundError("Sale not found")
        return sale

    async def add_item(self, sale_id: int, barcode: str, amount: int):
        sale = await self.repo.get_sale(sale_id)
        if not sale:
            raise NotFoundError("Sale not found")
        if sale.status != SaleStatus.OPEN:
            raise ConflictError("Sale is not OPEN")
        await self.repo.add_line(sale_id, barcode, amount)
        return BooleanResponseDTO(success=True)

    async def remove_item(self, sale_id: int, barcode: str, amount: int):
        ok = await self.repo.remove_line(sale_id, barcode, amount)
        if not ok:
            raise NotFoundError("Item not found")
        return BooleanResponseDTO(success=True)

    async def set_discount(self, sale_id: int, discount: float):
        if discount < 0 or discount > 1:
            raise ConflictError("Discount must be between 0 and 1")
        ok = await self.repo.set_discount(sale_id, discount)
        if not ok:
            raise NotFoundError("Sale not found")
        return BooleanResponseDTO(success=True)

    async def close_sale(self, sale_id: int):
        ok = await self.repo.set_status(sale_id, SaleStatus.PENDING)
        if not ok:
            raise NotFoundError("Sale not found")
        return BooleanResponseDTO(success=True)
