from typing import List
import re

from app.repositories.order_repository import OrderRepository
from app.models.DTO.order_dto import (
    OrderCreateDTO,
    OrderPayForDTO,
    OrderResponseDTO,
    OrderPaymentDTO,
    OrderArrivalDTO,
)
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.DAO.order_dao import OrderDAO


class OrderService:
    def __init__(self):
        self.repo = OrderRepository()

    def _validate_id(self, id: int, entity_name: str = "ID") -> None:
        if id <= 0:
            raise BadRequestError(f"{entity_name} must be greater than 0")

    def _validate_barcode(self, barcode: str) -> None:
        if not barcode or len(barcode.strip()) == 0:
            raise BadRequestError("Product barcode cannot be empty")
        if not re.match(r"^\d{12,14}$", barcode):
            raise BadRequestError("Barcode must be a string of 12-14 digits")

    def _validate_quantity(self, quantity: int) -> None:
        if quantity <= 0:
            raise BadRequestError("Quantity must be greater than 0")

    def _validate_price(self, price: float) -> None:
        if price <= 0:
            raise BadRequestError("Price per unit must be greater than 0")

    async def _get_order(self, order_id: int) -> OrderDAO:
        self._validate_id(order_id, "Order ID")
        order = await self.repo.get_order_by_id(order_id)
        if not order:
            raise NotFoundError(f"Order with id '{order_id}' not found")
        return order

    def _to_order_response(self, order: OrderDAO) -> OrderResponseDTO:
        return OrderResponseDTO(
            id=order.id,
            product_barcode=order.product_barcode,
            quantity=order.quantity,
            price_per_unit=order.price_per_unit,
            status=order.status,
            issue_date=order.issue_date,
        )

    async def create_order(self, order_dto: OrderCreateDTO) -> OrderResponseDTO:
        self._validate_barcode(order_dto.product_barcode)
        self._validate_quantity(order_dto.quantity)
        self._validate_price(order_dto.price_per_unit)

        try:
            created_order = await self.repo.create_order(order_dto)
            if not created_order:
                raise Exception("Failed to create order")
            return self._to_order_response(created_order)
        except ValueError as e:
            raise NotFoundError(str(e))

    async def list_orders(self) -> List[OrderResponseDTO]:
        orders = await self.repo.list_orders()
        return [self._to_order_response(o) for o in orders]

    async def create_and_pay_order(self, order_dto: OrderPayForDTO) -> OrderResponseDTO:
        self._validate_barcode(order_dto.product_barcode)
        self._validate_quantity(order_dto.quantity)

        try:
            created_order = await self.repo.create_and_pay_order(order_dto)
            if not created_order:
                raise Exception("Failed to create and pay order")
            return self._to_order_response(created_order)
        except ValueError as e:
            raise NotFoundError(str(e))


    async def pay_order(self, order_id: int, payment_dto: OrderPaymentDTO) -> OrderResponseDTO:
        await self._get_order(order_id)
        
        updated_order = await self.repo.pay_order(order_id)
        if not updated_order:
            raise NotFoundError(f"Order with id '{order_id}' not found")
        return self._to_order_response(updated_order)


    async def record_order_arrival(
        self, order_id: int, arrival_dto: OrderArrivalDTO
    ) -> OrderResponseDTO:
        await self._get_order(order_id)
        
        try:
            updated_order = await self.repo.record_order_arrival(order_id)
            if not updated_order:
                raise NotFoundError(f"Order with id '{order_id}' not found")
            return self._to_order_response(updated_order)
        except ValueError as e:
            raise NotFoundError(str(e))