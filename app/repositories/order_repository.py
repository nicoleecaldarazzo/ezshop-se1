from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime, timezone
from app.database.database import AsyncSessionLocal
from app.models.DAO.order_dao import OrderDAO
from app.models.DAO.product_dao import ProductDAO
from app.models.DTO.order_dto import OrderCreateDTO, OrderPayForDTO
from app.models.errors.conflict_error import ConflictError
from app.models.order_status import OrderStatus


class OrderRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session

    async def _get_session(self) -> AsyncSession:
        return self._session or AsyncSessionLocal()



    async def create_order(self, order_dto: OrderCreateDTO) -> OrderDAO:

        async with await self._get_session() as session:

            res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == order_dto.product_barcode)
            )
            product = res.scalar_one_or_none()
            if not product:
                raise ValueError("Product not found")

            order = OrderDAO(
                product_barcode=order_dto.product_barcode,
                quantity=order_dto.quantity,
                price_per_unit=order_dto.price_per_unit,
                status=OrderStatus.ISSUED,
                issue_date=datetime.now(timezone.utc)
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def list_orders(self) -> list[OrderDAO]:

        async with await self._get_session() as session:
            res = await session.execute(select(OrderDAO))
            return list(res.scalars().all())

    async def get_order_by_id(self, order_id: int) -> Optional[OrderDAO]:

        async with await self._get_session() as session:
            return await session.get(OrderDAO, order_id)



    async def create_and_pay_order(self, dto: OrderPayForDTO) -> OrderDAO:

        async with await self._get_session() as session:

            res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == dto.product_barcode)
            )
            product = res.scalar_one_or_none()
            if not product:
                raise ValueError("Product not found")


            order = OrderDAO(
                product_barcode=dto.product_barcode,
                quantity=dto.quantity,
                price_per_unit=product.price_per_unit,  
                status=OrderStatus.PAID,
                issue_date=datetime.now(timezone.utc)
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def pay_order(self, order_id: int) -> Optional[OrderDAO]:

        async with await self._get_session() as session:
            order = await session.get(OrderDAO, order_id)
            if not order:
                return None


            if order.status != OrderStatus.ISSUED:
                raise ConflictError(f"Order must be in ISSUED state to be paid (current: {order.status})")


            order.status = OrderStatus.PAID

            await session.commit()
            await session.refresh(order)
            return order

    async def record_order_arrival(self, order_id: int) -> Optional[OrderDAO]:

        async with await self._get_session() as session:
            order = await session.get(OrderDAO, order_id)
            if not order:
                return None

            if order.status != OrderStatus.PAID:
                raise ConflictError(f"Order must be in PAID state to record arrival (current: {order.status})")


            res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == order.product_barcode)
            )
            product = res.scalar_one_or_none()
            if not product:
                raise ValueError("Product not found")

            product.quantity += order.quantity


            order.status = OrderStatus.COMPLETED

            await session.commit()
            await session.refresh(order)
            await session.refresh(product)
            return order