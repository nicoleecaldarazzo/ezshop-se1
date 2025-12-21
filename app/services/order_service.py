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

    # --------------------
    # Validators
    # --------------------

    def _validate_id(self, id: int, entity_name: str = "ID") -> None:
        if id <= 0:
            raise BadRequestError(f"{entity_name} must be greater than 0")

    def _validate_barcode(self, barcode: str) -> None:
        """Validate barcode format (12-14 digits)"""
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

    # --------------------
    # Internal helpers
    # --------------------

    async def _get_order(self, order_id: int) -> OrderDAO:
        """Get order by ID or raise NotFoundError"""
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

    # --------------------
    # Orders (CRUD-like operations)
    # --------------------

    async def create_order(self, order_dto: OrderCreateDTO) -> OrderResponseDTO:
        """
        POST /orders - Issue a new order.
        The order is created with status ISSUED.
        """
        # Validate input
        self._validate_barcode(order_dto.product_barcode)
        self._validate_quantity(order_dto.quantity)
        self._validate_price(order_dto.price_per_unit)

        # Create order (repository handles product existence check via ValueError)
        try:
            created_order = await self.repo.create_order(order_dto)
            if not created_order:
                raise Exception("Failed to create order")
            return self._to_order_response(created_order)
        except ValueError as e:
            raise NotFoundError(str(e))

    async def list_orders(self) -> List[OrderResponseDTO]:
        """GET /orders - List all orders"""
        orders = await self.repo.list_orders()
        return [self._to_order_response(o) for o in orders]

    # --------------------
    # Order operations
    # --------------------

    async def create_and_pay_order(self, order_dto: OrderPayForDTO) -> OrderResponseDTO:
        """
        POST /orders/payfor - Create and pay an order for a product.
        The order is created with status PAID directly.
        Uses the current product price automatically.
        """
        # Validate input
        self._validate_barcode(order_dto.product_barcode)
        self._validate_quantity(order_dto.quantity)

        # Create and pay order (repository handles product existence and gets price)
        try:
            created_order = await self.repo.create_and_pay_order(order_dto)
            if not created_order:
                raise Exception("Failed to create and pay order")
            return self._to_order_response(created_order)
        except ValueError as e:
            raise NotFoundError(str(e))

    async def pay_order(self, order_id: int, payment_dto: OrderPaymentDTO) -> OrderResponseDTO:
        """
        PATCH /orders/{order_id}/pay - Pay for an existing ISSUED order.
        Changes order status from ISSUED to PAID.
        """
        # Validate order exists first
        await self._get_order(order_id)

        # Pay order (repository handles status validation via ConflictError)
        try:
            updated_order = await self.repo.pay_order(order_id)
            if not updated_order:
                raise NotFoundError(f"Order with id '{order_id}' not found")
            return self._to_order_response(updated_order)
        except ConflictError:
            raise  # Re-raise conflict error from repository

    async def record_order_arrival(
        self, order_id: int, arrival_dto: OrderArrivalDTO
    ) -> OrderResponseDTO:
        """
        PATCH /orders/{order_id}/arrival - Record the arrival of a PAID order.
        Changes order status from PAID to COMPLETED and increases product quantity.
        """
        # Validate order exists first
        await self._get_order(order_id)

        # Record arrival (repository handles status validation and product update)
        try:
            updated_order = await self.repo.record_order_arrival(order_id)
            if not updated_order:
                raise NotFoundError(f"Order with id '{order_id}' not found")
            return self._to_order_response(updated_order)
        except ConflictError:
            raise  # Re-raise conflict error from repository
        except ValueError as e:
            raise NotFoundError(str(e))