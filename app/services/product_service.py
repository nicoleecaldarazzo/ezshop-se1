from typing import List, Optional
import re

from app.repositories.product_repository import ProductRepository
from app.models.DTO.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductResponseDTO,
    ProductPositionUpdateDTO,
    ProductSearchDTO,
)
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.DAO.product_dao import ProductDAO


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    # --------------------
    # Validators
    # --------------------

    def _validate_id(self, id: int, entity_name: str = "ID") -> None:
        if id <= 0:
            raise BadRequestError(f"{entity_name} must be greater than 0")

    def _validate_barcode(self, barcode: str) -> None:
        """Validate barcode format (12-14 digits)"""
        if not re.match(r"^\d{12,14}$", barcode):
            raise BadRequestError("Barcode must be a string of 12-14 digits")

    def _validate_price(self, price: float) -> None:
        if price <= 0:
            raise BadRequestError("Price per unit must be greater than 0")

    def _validate_quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise BadRequestError("Quantity cannot be negative")

    def _validate_position(self, position: Optional[str]) -> None:
        """Validate position format (aisle-shelf-level or empty to clear)"""
        if position is not None and position != "":
            # Pattern: number-letter-number (e.g., "1-A-2")
            if not re.match(r"^\d+-[A-Za-z]-\d+$", position):
                raise BadRequestError(
                    "Position must match pattern 'aisle-shelf-level' (e.g., '1-A-2')"
                )

    # --------------------
    # Internal helpers
    # --------------------

    async def _get_product(self, product_id: int) -> ProductDAO:
        self._validate_id(product_id, "Product ID")
        product = await self.repo.get_product_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id '{product_id}' not found")
        return product

    def _to_product_response(self, product: ProductDAO) -> ProductResponseDTO:
        return ProductResponseDTO(
            id=product.id,
            description=product.description,
            barcode=product.barcode,
            price_per_unit=product.price_per_unit,
            note=product.note,
            quantity=product.quantity,
            position=product.position,
        )

    # --------------------
    # Business Logic Validators
    # --------------------

    async def _validate_product_can_be_deleted(self, product: ProductDAO) -> None:
        """
        Validates that a product can be deleted.
        A product cannot be deleted if it has:
        - Sales (OPEN, PENDING, or PAID)
        - Orders (ISSUED, PAID, or COMPLETED)
        - Returns (OPEN, CLOSED, or REIMBURSED)
        """
        has_sales = await self.repo.has_active_sales(product.barcode)
        has_orders = await self.repo.has_active_orders(product.barcode)
        has_returns = await self.repo.has_active_returns(product.barcode)

        errors = []
        if has_sales:
            errors.append("sales (OPEN, PENDING, or PAID)")
        if has_orders:
            errors.append("orders (ISSUED, PAID, or COMPLETED)")
        if has_returns:
            errors.append("returns (OPEN, CLOSED, or REIMBURSED)")

        if errors:
            raise ConflictError(
                f"Product cannot be deleted because it has active {', '.join(errors)}"
            )

    async def _validate_barcode_can_be_updated(
        self, current_barcode: str
    ) -> None:
        """
        Validates that a product's barcode can be updated.
        Barcode can be updated only if the product has:
        - NO sales associated with it
        - NO orders associated with it
        - NO returns associated with it
        """
        has_sales = await self.repo.has_active_sales(current_barcode)
        has_orders = await self.repo.has_active_orders(current_barcode)
        has_returns = await self.repo.has_active_returns(current_barcode)

        errors = []
        if has_sales:
            errors.append("sales")
        if has_orders:
            errors.append("orders")
        if has_returns:
            errors.append("returns")

        if errors:
            raise ConflictError(
                f"Product barcode cannot be updated because it has {', '.join(errors)} associated with it"
            )

    # --------------------
    # Products (CRUD)
    # --------------------

    async def create_product(self, product_dto: ProductCreateDTO) -> ProductResponseDTO:
        # Validate barcode format
        self._validate_barcode(product_dto.barcode)

        # Validate price
        self._validate_price(product_dto.price_per_unit)

        # Validate quantity
        self._validate_quantity(product_dto.quantity)

        # Validate position if provided
        if product_dto.position:
            self._validate_position(product_dto.position)

        # Create product (repository handles barcode conflict via ConflictError)
        created_product = await self.repo.create_product(product_dto)
        if not created_product:
            raise Exception("Failed to create product")

        return self._to_product_response(created_product)

    async def get_product(self, product_id: int) -> ProductResponseDTO:
        product = await self._get_product(product_id)
        return self._to_product_response(product)

    async def list_products(self) -> List[ProductResponseDTO]:
        products = await self.repo.list_products()
        return [self._to_product_response(p) for p in products]

    async def update_product(
        self, product_id: int, product_dto: ProductUpdateDTO
    ) -> ProductResponseDTO:
        self._validate_id(product_id, "Product ID")
        product = await self._get_product(product_id)

        # Validate fields if provided
        if product_dto.barcode is not None:
            self._validate_barcode(product_dto.barcode)
            # Check if barcode can be updated
            if product_dto.barcode != product.barcode:
                await self._validate_barcode_can_be_updated(product.barcode)

        if product_dto.price_per_unit is not None:
            self._validate_price(product_dto.price_per_unit)

        if product_dto.quantity is not None:
            self._validate_quantity(product_dto.quantity)

        if product_dto.position is not None:
            self._validate_position(product_dto.position)

        # Update product (repository handles barcode conflict via ConflictError)
        updated = await self.repo.update_product(product_id, product_dto)
        if not updated:
            raise NotFoundError(f"Product with id '{product_id}' not found")

        return self._to_product_response(updated)

    async def delete_product(self, product_id: int) -> bool:
        self._validate_id(product_id, "Product ID")
        product = await self._get_product(product_id)

        # Check if product can be deleted
        await self._validate_product_can_be_deleted(product)

        ok = await self.repo.delete_product(product_id)
        if not ok:
            raise NotFoundError(f"Product with id '{product_id}' not found")
        return ok

    # --------------------
    # Product operations (additional endpoints)
    # --------------------

    async def get_product_by_barcode(self, barcode: str) -> ProductResponseDTO:
        self._validate_barcode(barcode)
        product = await self.repo.get_product_by_barcode(barcode)
        if not product:
            raise NotFoundError(f"Product with barcode '{barcode}' not found")
        return self._to_product_response(product)

    async def search_products(self, search_dto: ProductSearchDTO) -> List[ProductResponseDTO]:
        if not search_dto.description or len(search_dto.description.strip()) == 0:
            raise BadRequestError("Search description cannot be empty")

        products = await self.repo.search_products_by_description(search_dto.description)
        return [self._to_product_response(p) for p in products]

    async def update_product_position(
        self, product_id: int, position_dto: ProductPositionUpdateDTO
    ) -> ProductResponseDTO:
        self._validate_id(product_id, "Product ID")
        await self._get_product(product_id)

        # Validate position format (empty string or None clears position)
        if position_dto.position:
            self._validate_position(position_dto.position)

        updated = await self.repo.update_product_position(product_id, position_dto)
        if not updated:
            raise NotFoundError(f"Product with id '{product_id}' not found")

        return self._to_product_response(updated)

    async def update_product_quantity(
        self, product_id: int, quantity_delta: int
    ) -> ProductResponseDTO:
        self._validate_id(product_id, "Product ID")
        await self._get_product(product_id)

        # Update quantity (repository validates non-negative result via ValueError)
        try:
            updated = await self.repo.update_product_quantity(product_id, quantity_delta)
            if not updated:
                raise NotFoundError(f"Product with id '{product_id}' not found")
            return self._to_product_response(updated)
        except ValueError as e:
            raise BadRequestError(str(e))