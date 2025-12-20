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

    # ---- Orders (CRUD-like operations) ----

    async def create_order(self, order_dto: OrderCreateDTO) -> OrderResponseDTO:
        """POST /orders - Issue a new order"""
        return await self.service.create_order(order_dto)

    async def list_orders(self) -> List[OrderResponseDTO]:
        """GET /orders - List all orders"""
        return await self.service.list_orders()

    # ---- Order operations ----

    async def create_and_pay_order(self, order_dto: OrderPayForDTO) -> OrderResponseDTO:
        """POST /orders/payfor - Create and pay an order for a product"""
        return await self.service.create_and_pay_order(order_dto)

    async def pay_order(self, order_id: int, payment_dto: OrderPaymentDTO) -> OrderResponseDTO:
        """PATCH /orders/{order_id}/pay - Pay for an existing issued order"""
        return await self.service.pay_order(order_id, payment_dto)

    async def record_order_arrival(
        self, order_id: int, arrival_dto: OrderArrivalDTO
    ) -> OrderResponseDTO:
        """PATCH /orders/{order_id}/arrival - Record the arrival of an order"""
        return await self.service.record_order_arrival(order_id, arrival_dto)