from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from app.database.database import AsyncSessionLocal
from app.models.DAO.customer_dao import CustomerDAO
from app.models.DAO.loyaltyCard_dao import LoyaltyCardDAO
from app.models.DTO.customer_dto import CustomerCreateDTO, CustomerUpdateDTO, LoyaltyCardCreateDTO, LoyaltyCardUpdateDTO
from app.models.errors.conflict_error import ConflictError


class CustomerRepository:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session

    async def _get_session(self) -> AsyncSession:
        return self._session or AsyncSessionLocal()

    async def get_customer_by_name(self, name: str) -> Optional[CustomerDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(CustomerDAO).where(CustomerDAO.name == name))
            return res.scalar_one_or_none()

    async def create_customer(self, customer_dto: CustomerCreateDTO) -> CustomerDAO:
        async with await self._get_session() as session:
            # id conflict check
            existing = await session.get(CustomerDAO, customer_dto.id)
            if existing:
                raise ConflictError("Customer ID already exists") 

            customer = CustomerDAO(id=customer_dto.id, name=customer_dto.name)
            session.add(customer)
            await session.commit()
            await session.refresh(customer)
            return customer

    async def list_customers(self) -> list[CustomerDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(CustomerDAO))
            return res.scalars().all()

    async def get_customer_by_id(self, id: int) -> Optional[CustomerDAO]:
        async with await self._get_session() as session:
            return await session.get(CustomerDAO, id)

    async def update_customer(self, id: int, dto: CustomerUpdateDTO) -> Optional[CustomerDAO]:
        async with await self._get_session() as session:
            # load with relationship (IMPORTANT for async)
            res = await session.execute(
                select(CustomerDAO)
                .options(selectinload(CustomerDAO.loyalty_card))
                .where(CustomerDAO.id == id)
            )
            customer = res.scalar_one_or_none()
            if not customer:
                return None

            # update name if provided
            if dto.name is not None:
                customer.name = dto.name

            # handle card rules
            # dto.card is:
            # - None  -> do nothing
            # - LoyaltyCardUpdateDTO(all None) -> treat as empty object {} -> detach+delete
            if dto.card is not None:
                is_empty_obj = (dto.card.card_id is None and dto.card.points is None)
                if is_empty_obj:
                    # detach + delete old card
                    if customer.loyalty_card is not None:
                        old_card = customer.loyalty_card
                        customer.loyalty_card = None
                        old_card.customer_id = None  # optional (safe)
                        await session.flush()        # ensures FK updates before delete
                        await session.delete(old_card)

                else:
                    # OPTIONAL: if you also want to allow updating points when card exists
                    if dto.card.points is not None:
                        if customer.loyalty_card is None:
                            # up to you: raise / ignore / create
                            # I'd raise in service layer; here just ignore or create logic.
                            pass
                        else:
                            customer.loyalty_card.points = dto.card.points

                    # OPTIONAL: if you want to change/attach card_id here, you need extra rules
                    # (find card by card_id, ensure not attached, detach old, attach new)

            await session.commit()

            # refresh with relationship again if you want response to contain card
            await session.refresh(customer)
            return customer

    async def delete_customer(self, id: int) -> bool:
        async with await self._get_session() as session:
            customer = await session.get(CustomerDAO, id)
            if not customer:
                return False
            await session.delete(customer)
            await session.commit()
            return True

    #  Swagger: POST /customers/cards (no customer_id)
    async def create_card(self, dto: LoyaltyCardCreateDTO) -> LoyaltyCardDAO:
        async with await self._get_session() as session:
            res = await session.execute(select(LoyaltyCardDAO).where(LoyaltyCardDAO.card_id == dto.card_id))
            if res.scalar_one_or_none():
                raise ConflictError("Card already exists")

            card = LoyaltyCardDAO(card_id=dto.card_id, points=dto.points, customer_id=None)
            session.add(card)
            await session.commit()
            await session.refresh(card)
            return card

    #  Swagger: PATCH /customers/{customer_id}/attach-card/{card_id}
    async def attach_card(self, customer_id: int, card_id: str) -> Optional[CustomerDAO]:
        async with await self._get_session() as session:
            customer = await session.get(CustomerDAO, customer_id)
            if not customer:
                return None

            res = await session.execute(select(LoyaltyCardDAO).where(LoyaltyCardDAO.card_id == card_id))
            card = res.scalar_one_or_none()
            if not card:
                return None

            # conflict checks
            if customer.loyalty_card is not None:
                raise ConflictError("Customer already has a card")  
            if card.customer_id is not None:
                raise ConflictError("Card already attached")        

            # attach
            card.customer_id = customer_id
            customer.loyalty_card = card   
            await session.commit()
            await session.refresh(card)
            await session.refresh(customer)
            return customer

    # Swagger: PATCH /customers/cards/{card_id}
    async def update_card_points(self, card_id: str, points: int) -> Optional[LoyaltyCardDAO]:
        async with await self._get_session() as session:
            res = await session.execute(select(LoyaltyCardDAO).where(LoyaltyCardDAO.card_id == card_id))
            card = res.scalar_one_or_none()
            if not card:
                return None
            card.points = points
            await session.commit()
            await session.refresh(card)
            return card
