from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database.database import AsyncSessionLocal
from app.models.DAO.product_dao import ProductDAO
from app.models.DTO.product_dto import ProductCreateDTO, ProductUpdateDTO, ProductPositionUpdateDTO
from app.models.errors.conflict_error import ConflictError


class ProductRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session

    async def _get_session(self) -> AsyncSession:
        return self._session or AsyncSessionLocal()


    async def create_product(self, product_dto: ProductCreateDTO) -> ProductDAO:
        """Create a new product type"""
        async with await self._get_session() as session:

            res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == product_dto.barcode)
            )
            existing = res.scalar_one_or_none()
            if existing:
                raise ConflictError("Product barcode already exists")

            product = ProductDAO(
                description=product_dto.description,
                barcode=product_dto.barcode,
                price_per_unit=product_dto.price_per_unit,
                note=product_dto.note,
                quantity=product_dto.quantity,
                position=product_dto.position
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    async def list_products(self) -> list[ProductDAO]:

        async with await self._get_session() as session:
            res = await session.execute(select(ProductDAO))
            return list(res.scalars().all())

    async def get_product_by_id(self, id: int) -> Optional[ProductDAO]:

        async with await self._get_session() as session:
            return await session.get(ProductDAO, id)

    async def get_product_by_barcode(self, barcode: str) -> Optional[ProductDAO]:

        async with await self._get_session() as session:
            res = await session.execute(
                select(ProductDAO).where(ProductDAO.barcode == barcode)
            )
            return res.scalar_one_or_none()

    async def search_products_by_description(self, description: str) -> list[ProductDAO]:

        async with await self._get_session() as session:
            res = await session.execute(
                select(ProductDAO).where(ProductDAO.description.ilike(f"%{description}%"))
            )
            return list(res.scalars().all())

    async def update_product(self, id: int, dto: ProductUpdateDTO) -> Optional[ProductDAO]:

        async with await self._get_session() as session:
            product = await session.get(ProductDAO, id)
            if not product:
                return None


            if dto.barcode is not None and dto.barcode != product.barcode:
                res = await session.execute(
                    select(ProductDAO).where(ProductDAO.barcode == dto.barcode)
                )
                if res.scalar_one_or_none():
                    raise ConflictError("Barcode already exists")


            if dto.description is not None:
                product.description = dto.description
            if dto.barcode is not None:
                product.barcode = dto.barcode
            if dto.price_per_unit is not None:
                product.price_per_unit = dto.price_per_unit
            if dto.note is not None:
                product.note = dto.note
            if dto.quantity is not None:
                product.quantity = dto.quantity
            if dto.position is not None:
                product.position = dto.position

            await session.commit()
            await session.refresh(product)
            return product

    async def delete_product(self, id: int) -> bool:

        async with await self._get_session() as session:
            product = await session.get(ProductDAO, id)
            if not product:
                return False
            await session.delete(product)
            await session.commit()
            return True


    async def update_product_position(
        self, id: int, dto: ProductPositionUpdateDTO
    ) -> Optional[ProductDAO]:

        async with await self._get_session() as session:
            product = await session.get(ProductDAO, id)
            if not product:
                return None


            product.position = dto.position

            await session.commit()
            await session.refresh(product)
            return product

    async def update_product_quantity(self, id: int, quantity_delta: int) -> Optional[ProductDAO]:

        async with await self._get_session() as session:
            product = await session.get(ProductDAO, id)
            if not product:
                return None


            new_quantity = product.quantity + quantity_delta
            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative")

            product.quantity = new_quantity

            await session.commit()
            await session.refresh(product)
            return product



    async def has_active_sales(self, product_barcode: str) -> bool:

        async with await self._get_session() as session:
            from app.models.DAO.sale_line_dao import SaleLineDAO
            from app.models.DAO.sale_dao import SaleDAO
            from app.models.sale_status import SaleStatus
            
            res = await session.execute(
                select(SaleLineDAO)
                .join(SaleDAO, SaleLineDAO.sale_id == SaleDAO.id)
                .where(
                    SaleLineDAO.product_barcode == product_barcode,
                    SaleDAO.status.in_([SaleStatus.OPEN, SaleStatus.PENDING, SaleStatus.PAID])
                )
            )
            return res.scalar_one_or_none() is not None

    async def has_active_orders(self, product_barcode: str) -> bool:

        async with await self._get_session() as session:
            from app.models.DAO.order_dao import OrderDAO
            from app.models.order_status import OrderStatus
            
            res = await session.execute(
                select(OrderDAO).where(
                    OrderDAO.product_barcode == product_barcode,
                    OrderDAO.status.in_([OrderStatus.ISSUED, OrderStatus.PAID, OrderStatus.COMPLETED])
                )
            )
            return res.scalar_one_or_none() is not None

    async def has_active_returns(self, product_barcode: str) -> bool:

        async with await self._get_session() as session:
            from app.models.DAO.return_dao import ReturnLineDAO
            from app.models.DAO.return_dao import ReturnDAO
            from app.models.return_status import ReturnStatus
            
            res = await session.execute(
                select(ReturnLineDAO)
                .join(ReturnDAO, ReturnLineDAO.return_id == ReturnDAO.id)
                .where(
                    ReturnLineDAO.product_barcode == product_barcode,
                    ReturnDAO.status.in_([ReturnStatus.OPEN, ReturnStatus.CLOSED, ReturnStatus.REIMBURSED])
                )
            )
            return res.scalar_one_or_none() is not None