from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.database import AsyncSessionLocal
from app.models.DAO.return_dao import ReturnDAO, ReturnLineDAO
from app.models.return_status import ReturnStatus
from datetime import datetime, timezone

class ReturnRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session

    async def _get_session(self) -> AsyncSession:
        return self._session or AsyncSessionLocal()

    async def create_return(self, sale_id: int) -> ReturnDAO:
        async with await self._get_session() as session:
            new_return = ReturnDAO(sale_id=sale_id, status=ReturnStatus.OPEN)
            session.add(new_return)
            await session.commit()
            await session.refresh(new_return)
            return new_return

    async def get_return(self, return_id: int) -> Optional[ReturnDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(ReturnDAO).where(ReturnDAO.id == return_id))
            return res.scalar_one_or_none()

    async def list_returns(self) -> List[ReturnDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(ReturnDAO))
            return res.scalars().all()
    
    async def list_returns_by_sale(self, sale_id: int) -> List[ReturnDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(ReturnDAO).where(ReturnDAO.sale_id == sale_id))
            return res.scalars().all()

    async def delete_return(self, return_id: int) -> bool:
        async with await self._get_session() as session:
            ret = await session.get(ReturnDAO, return_id)
            if not ret: return False
            await session.delete(ret)
            await session.commit()
            return True

    async def add_item(self, return_id: int, barcode: str, quantity: int, price: float) -> bool:
        async with await self._get_session() as session:
            line = ReturnLineDAO(return_id=return_id, product_barcode=barcode, quantity=quantity, price_per_unit=price)
            session.add(line)
            await session.commit()
            return True

    async def remove_item(self, return_id: int, barcode: str, quantity: int) -> bool:
        async with await self._get_session() as session:
            res = await session.execute(select(ReturnLineDAO).where(
                ReturnLineDAO.return_id == return_id,
                ReturnLineDAO.product_barcode == barcode
            ))
            line = res.scalars().first()
            
            if not line:
                return False

            if line.quantity > quantity:
                line.quantity -= quantity
            else:
                await session.delete(line)
            
            await session.commit()
            return True

    async def close_return(self, return_id: int) -> Optional[ReturnDAO]:
        async with await self._get_session() as session:
            ret = await session.get(ReturnDAO, return_id)
            if not ret: return None
            ret.status = ReturnStatus.CLOSED
            ret.closed_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(ret)
            return ret

    async def reimburse_return(self, return_id: int) -> Optional[ReturnDAO]:
        async with await self._get_session() as session:
            ret = await session.get(ReturnDAO, return_id)
            if not ret: return None
            ret.status = ReturnStatus.REIMBURSED
            await session.commit()
            await session.refresh(ret)
            return ret