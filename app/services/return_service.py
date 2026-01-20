from typing import List
from fastapi import HTTPException
from app.repositories.return_repository import ReturnRepository
from app.repositories.system_repository import SystemRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.sale_repository import SaleRepository

from app.models.DTO.return_dto import ReturnDTO, ReturnLineDTO
from app.models.return_status import ReturnStatus
from app.models.sale_status import SaleStatus 
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError

class ReturnService:
    def __init__(self):
        self.repo = ReturnRepository()
        self.accounting_repo = SystemRepository()
        self.product_repo = ProductRepository() 
        self.sale_repo = SaleRepository()       

    def _to_dto(self, dao) -> ReturnDTO:
        lines = [ReturnLineDTO(
            id=l.id, product_barcode=l.product_barcode, quantity=l.quantity, price_per_unit=l.price_per_unit
        ) for l in dao.lines]
        return ReturnDTO(
            id=dao.id, sale_id=dao.sale_id, status=dao.status, 
            lines=lines, created_at=dao.created_at, closed_at=dao.closed_at
        )

    async def create_return(self, sale_id: int) -> ReturnDTO:
        if sale_id <= 0:
            raise BadRequestError("Invalid sale ID")

        # Step 1: Check if sale exists (404)
        sale = await self.sale_repo.get_sale(sale_id)
        if not sale:
            raise NotFoundError(f"Sale {sale_id} not found")

        # Step 2: Check if sale is PAID (420)
        if getattr(sale, 'status', None) != SaleStatus.PAID:
            raise HTTPException(status_code=420, detail="Return allowed only on paid sales")
        
        dao = await self.repo.create_return(sale_id)
        return self._to_dto(dao)

    async def get_return(self, return_id: int) -> ReturnDTO:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        return self._to_dto(dao)

    async def list_returns(self) -> List[ReturnDTO]:
        daos = await self.repo.list_returns()
        return [self._to_dto(d) for d in daos]

    async def list_returns_by_sale(self, sale_id: int) -> List[ReturnDTO]:
        daos = await self.repo.list_returns_by_sale(sale_id)
        return [self._to_dto(d) for d in daos]

    async def delete_return(self, return_id: int) -> bool:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        
        if dao.status == ReturnStatus.REIMBURSED:
            raise HTTPException(status_code=420, detail="Cannot delete a reimbursed return")
        
        return await self.repo.delete_return(return_id)

    async def add_item(self, return_id: int, barcode: str, amount: int) -> bool:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")

        if dao.status != ReturnStatus.OPEN:
            raise HTTPException(status_code=420, detail="Cannot modify a closed return")

        sale = await self.sale_repo.get_sale(dao.sale_id)
        if not sale:
            raise NotFoundError("Associated sale not found")
        
        found_line = None
        # Locate the specific line item in the original sale
        for line in getattr(sale, 'lines', []):
            item_barcode = getattr(line, 'product_barcode', None)
            if item_barcode == barcode:
                found_line = line
                break
        
        if not found_line:
            raise BadRequestError("Product not found in the original sale")

        if amount > found_line.quantity:
            raise BadRequestError(f"Cannot return {amount} items. Only {found_line.quantity} were sold.")

        price = 0.0 
        return await self.repo.add_item(return_id, barcode, amount, price)

    async def remove_item(self, return_id: int, barcode: str, amount: int) -> bool:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        
        if dao.status != ReturnStatus.OPEN:
            raise HTTPException(status_code=420, detail="Cannot remove items from a closed return")
        
        return await self.repo.remove_item(return_id, barcode, amount)

    async def close_return(self, return_id: int) -> bool:
        return_tx = await self.repo.get_return(return_id)
        if not return_tx:
            raise NotFoundError(f"Return with id {return_id} not found")

        if return_tx.status != ReturnStatus.OPEN:
            raise HTTPException(status_code=420, detail="Return is not in OPEN state")

        for line in return_tx.lines:
            product = await self.product_repo.get_product_by_barcode(line.product_barcode)
            if product:
                await self.product_repo.update_product_quantity(product.id, line.quantity)

        await self.repo.close_return(return_id)
        return True

    async def reimburse_return(self, return_id: int) -> dict:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        
        if dao.status != ReturnStatus.CLOSED:
            raise HTTPException(status_code=420, detail="Return must be closed before reimbursement")

        total_refund = sum(line.quantity * line.price_per_unit for line in dao.lines)

        await self.accounting_repo.update_balance(-total_refund)
        await self.repo.reimburse_return(return_id)
        
        return {"refund_amount": total_refund}