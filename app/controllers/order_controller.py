from typing import List

from app.services.order_service import OrderService
from app.models.DTO.order_dto import (
    OrderCreateDTO,
    OrderPayForDTO,
    OrderResponseDTO,
    OrderPaymentDTO,
    OrderArrivalDTO,
)


class OrderController:
    def __init__(self):
        self.service = OrderService()


    async def create_order(self, order_dto: OrderCreateDTO) -> OrderResponseDTO:
        return await self.service.create_order(order_dto)

    async def list_orders(self) -> List[OrderResponseDTO]:
        return await self.service.list_orders()


    async def create_and_pay_order(self, order_dto: OrderPayForDTO) -> OrderResponseDTO:
        return await self.service.create_and_pay_order(order_dto)

    async def pay_order(self, order_id: int, payment_dto: OrderPaymentDTO) -> OrderResponseDTO:
        return await self.service.pay_order(order_id, payment_dto)

    async def record_order_arrival(
        self, order_id: int, arrival_dto: OrderArrivalDTO
    ) -> OrderResponseDTO:
        return await self.service.record_order_arrival(order_id, arrival_dto)