from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime

from app.database.database import AsyncSessionLocal
from app.models.DAO.sale_dao import SaleDAO
from app.models.DAO.sale_line_dao import SaleLineDAO
from app.models.sale_status import SaleStatus

class SaleRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session

    async def _get_session(self) -> AsyncSession:
        return self._session or AsyncSessionLocal()

    async def create_sale(self) -> SaleDAO:
        async with await self._get_session() as session:
            sale = SaleDAO()
            session.add(sale)
            await session.commit()
            await session.refresh(sale)
            return sale

    async def get_sale(self, sale_id: int) -> Optional[SaleDAO]:
        async with await self._get_session() as session:
            res = await session.execute(
                select(SaleDAO)
                .options(selectinload(SaleDAO.lines))
                .where(SaleDAO.id == sale_id)
            )
            return res.scalar_one_or_none()

    async def add_line(self, sale_id: int, barcode: str, amount: int) -> bool:
        async with await self._get_session() as session:
            line = SaleLineDAO(
                sale_id=sale_id,
                product_barcode=barcode,
                quantity=amount,
                price_per_unit=0.0
            )
            session.add(line)
            await session.commit()
            return True

    async def remove_line(self, sale_id: int, barcode: str, amount: int) -> bool:
        async with await self._get_session() as session:
            res = await session.execute(
                select(SaleLineDAO).where(
                    SaleLineDAO.sale_id == sale_id,
                    SaleLineDAO.product_barcode == barcode
                )
            )
            line = res.scalar_one_or_none()
            if not line:
                return False

            if line.quantity > amount:
                line.quantity -= amount
            else:
                await session.delete(line)

            await session.commit()
            return True

    async def set_discount(self, sale_id: int, discount: float) -> bool:
        async with await self._get_session() as session:
            sale = await session.get(SaleDAO, sale_id)
            if not sale:
                return False
            sale.discount_rate = discount
            await session.commit()
            return True

    async def set_status(self, sale_id: int, status: SaleStatus) -> bool:
        async with await self._get_session() as session:
            sale = await session.get(SaleDAO, sale_id)
            if not sale:
                return False
            sale.status = status
            if status == SaleStatus.PENDING and sale.closed_at is None:
                sale.closed_at = datetime.utcnow()
            await session.commit()
            return True
