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
from app.models.errors.invalid_state_error import InvalidStateError
from app.models.DAO.product_dao import ProductDAO


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def _validate_id(self, id: int, entity_name: str = "ID") -> None:
        if id <= 0:
            raise BadRequestError(f"{entity_name} must be greater than 0")

    import re

    def _validate_barcode(self, barcode: str) -> None:
        if not (isinstance(barcode, str) and re.match(r"^\d{12,14}$", barcode)):
            raise BadRequestError("Barcode must be a string of 12-14 digits")
        provided_check_digit = int(barcode[-1])
        payload_digits = list(map(int, barcode[:-1]))[::-1]
        total_sum = 0
        for i, digit in enumerate(payload_digits):
            if i % 2 == 0:
                total_sum += digit * 3
            else:
                total_sum += digit * 1
        calculated_check_digit = (10 - (total_sum % 10)) % 10
        if provided_check_digit != calculated_check_digit:
            raise BadRequestError(
                f"Invalid barcode: check digit mismatch. "
                f"Expected {calculated_check_digit} based on GS1 algorithm."
            )

    def _validate_price(self, price: float) -> None:
        if price <= 0:
            raise BadRequestError("Price per unit must be greater than 0")

    def _validate_quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise BadRequestError("Quantity cannot be negative")

    def _validate_position(self, position: Optional[str]) -> None:

        if position is not None and position != "":

            if not re.match(r"^\d+-[A-Za-z]-\d+$", position):
                raise BadRequestError(
                    "Position must match pattern 'aisle-shelf-level' (e.g., '1-A-2')"
                )

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

    async def _validate_product_can_be_deleted(self, product: ProductDAO) -> None:

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
            raise InvalidStateError(
                f"Product cannot be deleted because it has active {', '.join(errors)}"
            )         

    async def _validate_barcode_can_be_updated(self, current_barcode: str) -> None:

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

    async def create_product(self, product_dto: ProductCreateDTO) -> ProductResponseDTO:
        self._validate_barcode(product_dto.barcode)

        self._validate_price(product_dto.price_per_unit)

        self._validate_quantity(product_dto.quantity)

        if product_dto.position:
            self._validate_position(product_dto.position)

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


        # MODIFICA: Aggiungere validazione del formato del nuovo barcode
        if product_dto.barcode is not None:
            # Valida il formato del nuovo barcode
            self._validate_barcode(product_dto.barcode)
            
            # Se il barcode è diverso da quello esistente, controlla le transazioni
            if product_dto.barcode != product.barcode:
                await self._validate_barcode_can_be_updated(product.barcode)

        if product_dto.price_per_unit is not None:
            self._validate_price(product_dto.price_per_unit)

        if product_dto.quantity is not None:
            self._validate_quantity(product_dto.quantity)

        if product_dto.position is not None:
            self._validate_position(product_dto.position)

        updated = await self.repo.update_product(product_id, product_dto)
        if not updated:
            raise NotFoundError(f"Product with id '{product_id}' not found")

        return self._to_product_response(updated)

    async def delete_product(self, product_id: int) -> bool:
        self._validate_id(product_id, "Product ID")
        product = await self._get_product(product_id)

        await self._validate_product_can_be_deleted(product)

        ok = await self.repo.delete_product(product_id)
        if not ok:
            raise NotFoundError(f"Product with id '{product_id}' not found")
        return ok

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

    async def update_product_position(self, product_id: int, position_dto: ProductPositionUpdateDTO) -> ProductResponseDTO:
        self._validate_id(product_id, "Product ID")

        if position_dto.position:
            self._validate_position(position_dto.position)

        await self._get_product(product_id)

        updated = await self.repo.update_product_position(product_id, position_dto)
        if not updated:
            raise NotFoundError(f"Product with id '{product_id}' not found")

        return self._to_product_response(updated)

    async def update_product_quantity(
        self, product_id: int, quantity_delta: int
    ) -> ProductResponseDTO:
        self._validate_id(product_id, "Product ID")
        await self._get_product(product_id)

        try:
            updated = await self.repo.update_product_quantity(product_id, quantity_delta)
            if not updated:
                raise NotFoundError(f"Product with id '{product_id}' not found")
            return self._to_product_response(updated)
        except ValueError as e:
            raise BadRequestError(str(e))
        
    async def get_products_needing_reorder(self) -> List[ProductResponseDTO]:
        products = await self.repo.get_products_needing_reorder()
        return [self._to_product_response(p) for p in products]
        
