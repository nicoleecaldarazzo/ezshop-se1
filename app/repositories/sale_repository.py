from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timezone

from app.database.database import AsyncSessionLocal
from app.models.DAO.sale_dao import SaleDAO
from app.models.DAO.sale_line_dao import SaleLineDAO
from app.models.DAO.product_dao import ProductDAO 
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

    async def get_all_sales(self) -> List[SaleDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(SaleDAO).options(selectinload(SaleDAO.lines)))
            return res.scalars().all()

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
            prod_res = await session.execute(select(ProductDAO).where(ProductDAO.barcode == barcode))
            product = prod_res.scalar_one_or_none()
            
            if not product or product.quantity < amount:
                return False 

            product.quantity -= amount
            line_res = await session.execute(
                select(SaleLineDAO).where(SaleLineDAO.sale_id == sale_id, SaleLineDAO.product_barcode == barcode)
            )
            existing_line = line_res.scalar_one_or_none()

            if existing_line:
                existing_line.quantity += amount
            else:
                new_line = SaleLineDAO(
                    sale_id=sale_id,
                    product_barcode=barcode,
                    quantity=amount,
                    price_per_unit=product.price_per_unit
                )
                session.add(new_line)
            await session.commit()
            return True

    async def remove_line(self, sale_id: int, barcode: str, amount: int) -> bool:
        async with await self._get_session() as session:
            # 1. Fetch the sale line
            res = await session.execute(
                select(SaleLineDAO).where(
                    SaleLineDAO.sale_id == sale_id, 
                    SaleLineDAO.product_barcode == barcode
                )
            )
            line = res.scalar_one_or_none()
            
            if not line: 
                return False

            # --- CRITICAL ADDITION: RESTORE PRODUCT STOCK ---
            # When an item is removed from a sale, it must go back to the product inventory.
            prod_res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == barcode)
            )
            product = prod_res.scalar_one_or_none()
            if product:
                product.quantity += amount 

            # 2. Logic to update or delete the line
            if amount >= line.quantity:
                await session.delete(line)
            else:
                # This performs the subtraction the test is looking for
                line.quantity -= amount
                # Force SQLAlchemy to recognize the attribute change for the mock
                session.add(line) 
                
            await session.commit()
            return True
    async def delete_sale(self, sale_id: int) -> bool:
        async with await self._get_session() as session:
            res = await session.execute(
                select(SaleDAO).options(selectinload(SaleDAO.lines)).where(SaleDAO.id == sale_id)
            )
            sale = res.scalar_one_or_none()
            if not sale: return False
            
            # RESTORE STOCK for all items in the sale
            for line in (sale.lines or []):
                p_res = await session.execute(select(ProductDAO).where(ProductDAO.barcode == line.product_barcode))
                product = p_res.scalar_one_or_none()
                if product:
                    product.quantity += line.quantity
            
            await session.delete(sale)
            await session.commit()
            return True

    async def set_status(self, sale_id: int, status: SaleStatus) -> bool:
        async with await self._get_session() as session:
            sale = await session.get(SaleDAO, sale_id)
            if not sale: return False
            sale.status = status
            if status in [SaleStatus.PENDING, SaleStatus.PAID]:
                sale.closed_at = datetime.now(timezone.utc)
            await session.commit()
            return True
        
    async def set_discount(self, sale_id: int, discount: float) -> bool:
        async with await self._get_session() as session:
            # Use session.get for efficiency when looking up by PK
            sale = await session.get(SaleDAO, sale_id)
            if not sale:
                return False
            
            sale.discount_rate = discount
            await session.commit()
            return True

    async def set_line_discount(self, sale_id: int, barcode: str, discount: float) -> bool:
        async with await self._get_session() as session:
            # Find the specific line item for this sale and product
            res = await session.execute(
                select(SaleLineDAO).where(
                    SaleLineDAO.sale_id == sale_id, 
                    SaleLineDAO.product_barcode == barcode
                )
            )
            line = res.scalar_one_or_none()
            if not line:
                return False
            
            line.discount_rate = discount
            await session.commit()
            return True