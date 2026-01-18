from app.repositories.sale_repository import SaleRepository
from app.models.sale_status import SaleStatus
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.invalid_state_error import InvalidStateError

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

    async def remove_item(self, sale_id: int, barcode: str, amount: int):
        sale = await self.get_sale(sale_id)
        
        # Check if item exists in sale lines
        line = next((l for l in (sale.lines or []) if l.product_barcode == barcode), None)
        if not line:
            raise NotFoundError("Product not in sale")
        
        # FIXED: Returning 400 (BadRequest) instead of 404 for excessive removal
        if amount > line.quantity:
            raise BadRequestError("Cannot remove more items than present in sale")

        await self.repo.remove_line(sale_id, barcode, amount)
        return True

    async def close_sale(self, sale_id: int):
        sale = await self.get_sale(sale_id)
        
        # FIXED: Return 420 (InvalidState) if already PAID
        if sale.status == SaleStatus.PAID:
            raise InvalidStateError("Cannot close a sale that is already paid")
            
        if not sale.lines or len(sale.lines) == 0:
            await self.repo.delete_sale(sale_id)
            return True

        # Triggers repository to update 'closed_at'
        await self.repo.set_status(sale_id, SaleStatus.PENDING)
        return True
            
        if not sale.lines or len(sale.lines) == 0:
            await self.repo.delete_sale(sale_id)
            return True

        # Triggers repository to update 'closed_at'
        await self.repo.set_status(sale_id, SaleStatus.PENDING)
        return True
    async def pay_sale(self, sale_id: int, cash_amount: float):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.PENDING:
            raise InvalidStateError("Sale must be pending to pay")
            
        # Calculation logic...
        # change = cash - total
        await self.repo.set_status(sale_id, SaleStatus.PAID)
        return change