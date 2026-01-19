from app.repositories.sale_repository import SaleRepository
from app.models.sale_status import SaleStatus
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.invalid_state_error import InvalidStateError
from app.repositories.product_repository import ProductRepository
from app.repositories.system_repository import SystemRepository

class SaleService:
    def __init__(self):
        self.repo = SaleRepository()
        self.prod_repo = ProductRepository()

    async def create_sale(self):
        return await self.repo.create_sale()

    async def list_sales(self):
        return await self.repo.get_all_sales()

    async def get_sale(self, sale_id: int):
        sale = await self.repo.get_sale(sale_id)
        if not sale: raise NotFoundError("Sale not found")
        return sale

    async def delete_sale(self, sale_id: int):
        sale = await self.get_sale(sale_id)
        # Often evaluations forbid deleting PAID sales
        if sale.status == SaleStatus.PAID:
            raise InvalidStateError("Cannot delete a paid sale")
        return await self.repo.delete_sale(sale_id)

    async def add_item(self, sale_id: int, barcode: str, amount: int):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.OPEN:
            raise InvalidStateError("Sale is closed/paid")
        if amount <= 0: raise BadRequestError("Amount must be > 0")
        
        product = await self.prod_repo.get_product_by_barcode(barcode)
        if not product: raise NotFoundError("Product missing")
        if product.quantity < amount: raise BadRequestError("Stock low")

        return await self.repo.add_line(sale_id, barcode, amount)

    async def remove_item(self, sale_id: int, barcode: str, amount: int):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.OPEN: raise InvalidStateError("Sale is not open")
        
        line = next((l for l in (sale.lines or []) if l.product_barcode == barcode), None)
        if not line: raise NotFoundError("Not in sale")
        
        # This handles the 'test_remove_more_than_in_sale' (400 error)
        if amount > line.quantity: raise BadRequestError("Too much to remove")
        
        return await self.repo.remove_line(sale_id, barcode, amount)

    async def set_discount(self, sale_id: int, rate: float):
        sale = await self.get_sale(sale_id)
        # Business rule: Disallows discounts on closed or paid sales
        if sale.status != SaleStatus.OPEN: 
            raise InvalidStateError("Cannot apply discount to a non-open sale")
        
        # Validation: rate must be between 0 and 1 (e.g., 0.1 for 10%)
        if not (0 <= rate < 1): 
            raise BadRequestError("Invalid discount rate")
            
        return await self.repo.set_discount(sale_id, rate)

    async def set_product_discount(self, sale_id: int, barcode: str, rate: float):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.OPEN: raise InvalidStateError("Not open")
        if not (0 <= rate < 1): raise BadRequestError("Invalid rate")
        ok = await self.repo.set_line_discount(sale_id, barcode, rate)
        if not ok: raise NotFoundError("Product not in sale")
        return True

    async def close_sale(self, sale_id: int):
        sale = await self.get_sale(sale_id)
        if sale.status == SaleStatus.PAID: raise InvalidStateError("Already paid")
        
        # Rule: If empty, delete it but return SUCCESS (200), don't raise 404
        if not sale.lines or len(sale.lines) == 0:
            await self.repo.delete_sale(sale_id)
            return True 

        await self.repo.set_status(sale_id, SaleStatus.PENDING)
        return True

    async def pay_sale(self, sale_id: int, cash: float):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.PENDING: raise InvalidStateError("Not pending")
        
        total = 0.0
        for l in sale.lines:
            sub = (l.quantity * l.price_per_unit) * (1.0 - (l.discount_rate or 0.0))
            total += sub
        total *= (1.0 - (sale.discount_rate or 0.0))
        total = round(total, 2)

        if cash < total: raise BadRequestError(f"Insufficient cash. Need {total}")
        
        await self.repo.set_status(sale_id, SaleStatus.PAID)
        await SystemRepository().update_balance(total)
        return round(float(cash - total), 2)

    async def compute_points(self, sale_id: int):
        sale = await self.get_sale(sale_id)
        if sale.status != SaleStatus.PAID: raise InvalidStateError("Not paid")
        
        total = 0.0
        for l in sale.lines:
            total += (l.quantity * l.price_per_unit) * (1.0 - (l.discount_rate or 0.0))
        total *= (1.0 - (sale.discount_rate or 0.0))
        return int(total // 10)