from typing import List
from app.services.return_service import ReturnService
from app.models.DTO.return_dto import ReturnDTO

class ReturnController:
    def __init__(self):
        self.service = ReturnService()

    async def create_return(self, sale_id: int) -> ReturnDTO:
        return await self.service.create_return(sale_id)

    async def get_return(self, return_id: int) -> ReturnDTO:
        return await self.service.get_return(return_id)

    async def list_returns(self) -> List[ReturnDTO]:
        return await self.service.list_returns()
    
    async def list_returns_by_sale(self, sale_id: int) -> List[ReturnDTO]:
        return await self.service.list_returns_by_sale(sale_id)

    async def delete_return(self, return_id: int) -> bool:
        return await self.service.delete_return(return_id)

    async def add_item(self, return_id: int, barcode: str, amount: int) -> bool:
        return await self.service.add_item(return_id, barcode, amount)

    async def remove_item(self, return_id: int, barcode: str, amount: int) -> bool:
        return await self.service.remove_item(return_id, barcode, amount)

    async def close_return(self, return_id: int) -> dict:
        success = await self.service.close_return(return_id)
        return {"success": success}

    async def reimburse_return(self, return_id: int) -> dict:
        return await self.service.reimburse_return(return_id)
