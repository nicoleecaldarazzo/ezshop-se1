from typing import List
from app.services.customer_service import CustomerService
from app.models.DTO.customer_dto import (
    CustomerCreateDTO, CustomerUpdateDTO, CustomerResponseDTO,
    LoyaltyCardCreateDTO, LoyaltyCardPointsUpdateDTO, LoyaltyCardDTO
)

class CustomerController:
    def __init__(self):
        self.service = CustomerService()

    # ---- customers CRUD ----

    async def create_customer(self, customer_dto: CustomerCreateDTO) -> CustomerResponseDTO:
        return await self.service.create_customer(customer_dto)

    async def get_customer(self, customer_id: int) -> CustomerResponseDTO:
        return await self.service.get_customer(customer_id)

    async def list_customers(self) -> List[CustomerResponseDTO]:
        return await self.service.list_customers()

    async def update_customer(self, customer_id: int, customer_dto: CustomerUpdateDTO) -> CustomerResponseDTO:
        return await self.service.update_customer(customer_id, customer_dto)

    async def delete_customer(self, customer_id: int) -> bool:
        return await self.service.delete_customer(customer_id)

    # ---- loyalty endpoints (Swagger) ----

    # POST /customers/cards
    async def create_card(self, card_dto: LoyaltyCardCreateDTO) -> LoyaltyCardDTO:
        return await self.service.create_card(card_dto)

    # PATCH /customers/{customer_id}/attach-card/{card_id}
    async def attach_card(self, customer_id: int, card_id: str) -> CustomerResponseDTO:
        return await self.service.attach_card(customer_id, card_id)

    # PATCH /customers/cards/{card_id}
    async def update_card_points(self, card_id: str, points: int) -> LoyaltyCardDTO | None:
        return await self.service.update_card_points(card_id, points)



    # (Optional helper, not in your Swagger list but you had it)
    async def get_card(self, card_id: str) -> LoyaltyCardDTO:
        return await self.service.get_card(card_id)
