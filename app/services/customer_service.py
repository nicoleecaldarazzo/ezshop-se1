from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repositories.customer_repository import CustomerRepository
from app.models.DTO.customer_dto import (
    CustomerCreateDTO,
    CustomerUpdateDTO,
    CustomerResponseDTO,
    LoyaltyCardCreateDTO,
    LoyaltyCardPointsUpdateDTO,
    LoyaltyCardDTO,
)
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.customer_card_error import CustomerCardError

from app.models.DAO.customer_dao import CustomerDAO
from app.models.DAO.loyaltyCard_dao import LoyaltyCardDAO
from app.database.database import AsyncSessionLocal
import random

class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    def _generate_card_id(self) -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(10))

    def _validate_id(self, id: int, entity_name: str = "ID") -> None:
        if id <= 0:
            raise BadRequestError(f"{entity_name} must be greater than 0")

    def _validate_points(self, points: int) -> None:
        if points < 0:
            raise BadRequestError("Points cannot be negative")

    async def _get_customer(self, customer_id: int) -> CustomerDAO:
        self._validate_id(customer_id, "Customer ID")
        customer = await self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id '{customer_id}' not found")
        return customer

    async def create_customer_card(self) -> LoyaltyCardDTO:
        for _ in range(50):
            card_id = self._generate_card_id()
            existing = await self.repo.get_card_by_card_id(card_id)  
            if existing is None:
                created = await self.repo.create_card(LoyaltyCardCreateDTO(card_id=card_id, points=0))
                return LoyaltyCardDTO(card_id=created.card_id, points=created.points)
        raise Exception("Failed to generate unique card id")

    async def _get_customer_with_card(self, customer_id: int) -> CustomerDAO:
        self._validate_id(customer_id, "Customer ID")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(CustomerDAO)
                .options(selectinload(CustomerDAO.loyalty_card))
                .where(CustomerDAO.id == customer_id)
            )
            customer = result.scalar_one_or_none()
            if not customer:
                raise NotFoundError(f"Customer with id '{customer_id}' not found")
            return customer

    async def _get_card_by_card_id(self, card_id: str) -> Optional[LoyaltyCardDAO]:
        if not card_id:
            return None
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(LoyaltyCardDAO).where(LoyaltyCardDAO.card_id == card_id)
            )
            return result.scalar_one_or_none()

    async def _check_customer_has_card(self, customer_id: int) -> None:
        customer = await self._get_customer_with_card(customer_id)
        if customer.loyalty_card is not None:
            raise ConflictError(f"Customer with id '{customer_id}' already has a card")

    async def _check_card_attached(self, card: LoyaltyCardDAO) -> None:
        if card.customer_id is not None:
            raise ConflictError(f"Card with id '{card.card_id}' is already attached to a customer")

    def _to_customer_response(self, customer: CustomerDAO) -> CustomerResponseDTO:
        card_dto = None
        if getattr(customer, "loyalty_card", None):
            card_dto = LoyaltyCardDTO(
                card_id=customer.loyalty_card.card_id,
                points=customer.loyalty_card.points
            )
        return CustomerResponseDTO(
            id=customer.id,
            name=customer.name,
            card=card_dto
        )

    # Customers (CRUD)

    async def create_customer(self, customer_dto: CustomerCreateDTO) -> CustomerResponseDTO:
        existing_customer = await self.repo.get_customer_by_name(customer_dto.name)
        if existing_customer is not None:
            raise ConflictError(f"Customer with name '{customer_dto.name}' already exists")

        # create customer first
        created_customer = await self.repo.create_customer(customer_dto)
        if not created_customer:
            raise Exception("Failed to create customer")

        if customer_dto.card:
            existing_card = await self._get_card_by_card_id(customer_dto.card.card_id)
            if existing_card is None:
                raise ConflictError(f"Card with id '{customer_dto.card.card_id}' not found")

            if existing_card.customer_id is not None:
                raise ConflictError("Card already attached")

            await self.repo.attach_card(created_customer.id, existing_card.card_id)

        customer_full = await self._get_customer_with_card(created_customer.id)
        return self._to_customer_response(customer_full)


    async def get_customer(self, customer_id: int) -> CustomerResponseDTO:
        customer = await self._get_customer_with_card(customer_id)
        return self._to_customer_response(customer)

    async def list_customers(self) -> List[CustomerResponseDTO]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(CustomerDAO).options(selectinload(CustomerDAO.loyalty_card))
            )
            customers = result.scalars().all()
            return [self._to_customer_response(c) for c in customers]

    async def update_customer(self, customer_id: int, customer_dto: CustomerUpdateDTO) -> CustomerResponseDTO:
        self._validate_id(customer_id, "Customer ID")
        await self._get_customer(customer_id)

        updated = await self.repo.update_customer(customer_id, customer_dto)
        if not updated:
            raise NotFoundError(f"Customer with id '{customer_id}' not found")

        customer_full = await self._get_customer_with_card(customer_id)
        return self._to_customer_response(customer_full)

    async def delete_customer(self, customer_id: int) -> bool:
        self._validate_id(customer_id, "Customer ID")
        await self._get_customer(customer_id)

        ok = await self.repo.delete_customer(customer_id)
        if not ok:
            raise NotFoundError(f"Customer with id '{customer_id}' not found")
        return ok


    # POST /customers/cards
    async def create_card(self) -> LoyaltyCardDTO:
        for _ in range(50):
            card_id = self._generate_card_id()

            existing = await self._get_card_by_card_id(card_id)
            if existing is None:
                created = await self.repo.create_card(LoyaltyCardCreateDTO(card_id=card_id, points=0))
                return LoyaltyCardDTO(card_id=created.card_id, points=created.points)

        raise Exception("Failed to generate unique card id")

    # PATCH /customers/{customer_id}/attach-card/{card_id}
    async def attach_card(self, customer_id: int, card_id: str) -> CustomerResponseDTO:
        self._validate_id(customer_id, "Customer ID")
        if not card_id:
            raise BadRequestError("Card ID cannot be empty")

        await self._get_customer(customer_id)
        await self._check_customer_has_card(customer_id)

        card = await self._get_card_by_card_id(card_id)
        if not card:
            raise NotFoundError(f"Card with id '{card_id}' not found")

        await self._check_card_attached(card)

        updated_customer = await self.repo.attach_card(customer_id, card_id)
        if not updated_customer:
            raise Exception("Failed to attach card")

        customer_full = await self._get_customer_with_card(customer_id)
        return self._to_customer_response(customer_full)

    # PATCH /customers/cards/{card_id}
    async def update_card_points(self, card_id: str, points: int) -> LoyaltyCardDTO:
        if card_id is None or card_id == "":
            raise BadRequestError("Card ID must be an integer string")

        card = await self._get_card_by_card_id(card_id)
        if not card:
            raise NotFoundError(f"Customer Card not found")

        new_points = card.points + points
        if new_points < 0:
            raise CustomerCardError("Insufficient points on the card")
        updated = await self.repo.update_card_points(card_id, new_points)
        return LoyaltyCardDTO(card_id=updated.card_id, points=updated.points)


    async def get_card(self, card_id: str) -> LoyaltyCardDTO:
        if not card_id:
            raise BadRequestError("Card ID cannot be empty")

        card = await self._get_card_by_card_id(card_id)
        if not card:
            raise NotFoundError(f"Card with id '{card_id}' not found")

        return LoyaltyCardDTO(card_id=card.card_id, points=card.points)
