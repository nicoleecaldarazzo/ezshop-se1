from typing import List
from app.repositories.return_repository import ReturnRepository
from app.repositories.system_repository import SystemRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.sale_repository import SaleRepository

from app.models.DTO.return_dto import ReturnDTO, ReturnLineDTO
from app.models.return_status import ReturnStatus
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.conflict_error import ConflictError 

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
        # Checks if sale is PAID
        sale = await self.sale_repo.get_sale(sale_id)
        if not sale or getattr(sale, 'status', None) != "PAID":
            raise ConflictError("Return allowed only on paid sales")
        
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
            raise ConflictError("Cannot delete a reimbursed return")
        
        return await self.repo.delete_return(return_id)

    async def add_item(self, return_id: int, barcode: str, amount: int) -> bool:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")

        if dao.status != ReturnStatus.OPEN:
            raise ConflictError("Cannot modify a closed return")

        price = 0.0 
        return await self.repo.add_item(return_id, barcode, amount, price)

    async def remove_item(self, return_id: int, barcode: str, amount: int) -> bool:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        
        if dao.status != ReturnStatus.OPEN:
            raise ConflictError("Cannot remove items from a closed return")
        
        return await self.repo.remove_item(return_id, barcode, amount)

    async def close_return(self, return_id: int) -> bool:
        # Get the return transaction
        return_tx = await self.repo.get_return(return_id)
        if not return_tx:
            raise NotFoundError(f"Return with id {return_id} not found")

        # Check status (Must be OPEN to close)
        if return_tx.status != ReturnStatus.OPEN:
            raise ConflictError("Return is not in OPEN state")

        # Restock items (Loop through lines and update product quantity)
        for line in return_tx.lines:
            product = await self.product_repo.get_product_by_barcode(line.product_barcode)
            if product:
                await self.product_repo.update_product_quantity(product.id, line.quantity)

        # Close the return in DB
        await self.repo.close_return(return_id)
        return True

    async def reimburse_return(self, return_id: int) -> dict:
        dao = await self.repo.get_return(return_id)
        if not dao: raise NotFoundError("Return not found")
        
        if dao.status != ReturnStatus.CLOSED:
            raise ConflictError("Return must be closed before reimbursement")

        total_refund = sum(line.quantity * line.price_per_unit for line in dao.lines)

        await self.accounting_repo.update_balance(-total_refund)
        await self.repo.reimburse_return(return_id)
        
        return {"refund_amount": total_refund}