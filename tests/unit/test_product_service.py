import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.services.product_service import ProductService
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.notfound_error import NotFoundError


@pytest.fixture
def service():
    s = ProductService()

    s.repo = MagicMock()
    s.repo.create_product = AsyncMock()
    s.repo.list_products = AsyncMock()
    s.repo.get_product_by_id = AsyncMock()
    s.repo.get_product_by_barcode = AsyncMock()
    s.repo.search_products_by_description = AsyncMock()
    s.repo.update_product = AsyncMock()
    s.repo.delete_product = AsyncMock()
    s.repo.update_product_position = AsyncMock()
    s.repo.update_product_quantity = AsyncMock()
    s.repo.has_active_sales = AsyncMock()
    s.repo.has_active_orders = AsyncMock()
    s.repo.has_active_returns = AsyncMock()

    s._get_product = AsyncMock()

    return s


@pytest.mark.asyncio
async def test_create_product_ok(service):
    dto = SimpleNamespace(
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note="Test note",
        quantity=100,
        position="1-A-2"
    )

    created_product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note="Test note",
        quantity=100,
        position="1-A-2"
    )
    service.repo.create_product.return_value = created_product

    result = await service.create_product(dto)

    service.repo.create_product.assert_awaited_once_with(dto)
    assert result.id == 1
    assert result.description == "Test Product"
    assert result.barcode == "123456789012"
    assert result.price_per_unit == 10.5
    assert result.quantity == 100
    assert result.position == "1-A-2"


@pytest.mark.asyncio
async def test_create_product_invalid_barcode_raises(service):
    dto = SimpleNamespace(
        description="Test",
        barcode="123",
        price_per_unit=10.0,
        note=None,
        quantity=10,
        position=None
    )

    with pytest.raises(BadRequestError):
        await service.create_product(dto)

    service.repo.create_product.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_invalid_price_raises(service):
    dto = SimpleNamespace(
        description="Test",
        barcode="123456789012",
        price_per_unit=0,
        note=None,
        quantity=10,
        position=None
    )

    with pytest.raises(BadRequestError):
        await service.create_product(dto)

    service.repo.create_product.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_negative_quantity_raises(service):
    dto = SimpleNamespace(
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=-5,
        position=None
    )

    with pytest.raises(BadRequestError):
        await service.create_product(dto)

    service.repo.create_product.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_invalid_position_raises(service):
    dto = SimpleNamespace(
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=10,
        position="invalid-format"
    )

    with pytest.raises(BadRequestError):
        await service.create_product(dto)

    service.repo.create_product.assert_not_called()


@pytest.mark.asyncio
async def test_create_product_without_optional_fields(service):
    dto = SimpleNamespace(
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note=None,
        quantity=0,
        position=None
    )

    created_product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note=None,
        quantity=0,
        position=None
    )
    service.repo.create_product.return_value = created_product

    result = await service.create_product(dto)

    service.repo.create_product.assert_awaited_once_with(dto)
    assert result.note is None
    assert result.position is None


@pytest.mark.asyncio
async def test_get_product_invalid_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.get_product(0)

    service._get_product.assert_not_called()


@pytest.mark.asyncio
async def test_get_product_not_found_raises(service):
    service._get_product.side_effect = NotFoundError("Product not found")

    with pytest.raises(NotFoundError):
        await service.get_product(999)


@pytest.mark.asyncio
async def test_get_product_ok(service):
    dao = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note="Test note",
        quantity=100,
        position="1-A-2"
    )
    service._get_product.return_value = dao

    result = await service.get_product(1)

    service._get_product.assert_awaited_once_with(1)
    assert result.id == 1
    assert result.description == "Test Product"
    assert result.barcode == "123456789012"


@pytest.mark.asyncio
async def test_list_products_empty(service):
    service.repo.list_products.return_value = []

    result = await service.list_products()

    service.repo.list_products.assert_awaited_once()
    assert result == []


@pytest.mark.asyncio
async def test_list_products_multiple(service):
    products = [
        SimpleNamespace(id=1, description="P1", barcode="111111111111", 
                       price_per_unit=10.0, note=None, quantity=10, position=None),
        SimpleNamespace(id=2, description="P2", barcode="222222222222", 
                       price_per_unit=20.0, note=None, quantity=20, position=None)
    ]
    service.repo.list_products.return_value = products

    result = await service.list_products()

    service.repo.list_products.assert_awaited_once()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


@pytest.mark.asyncio
async def test_update_product_invalid_id_raises(service):
    dto = SimpleNamespace(description="New", barcode=None, price_per_unit=None, 
                         note=None, quantity=None, position=None)

    with pytest.raises(BadRequestError):
        await service.update_product(0, dto)


@pytest.mark.asyncio
async def test_update_product_not_found_raises(service):
    dto = SimpleNamespace(description="New", barcode=None, price_per_unit=None, 
                         note=None, quantity=None, position=None)
    service._get_product.side_effect = NotFoundError("not found")

    with pytest.raises(NotFoundError):
        await service.update_product(10, dto)


@pytest.mark.asyncio
async def test_update_product_ok(service):
    dto = SimpleNamespace(
        description="Updated Product",
        barcode=None,
        price_per_unit=15.0,
        note="Updated note",
        quantity=None,
        position=None
    )

    existing_product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = existing_product

    updated_product = SimpleNamespace(
        id=1,
        description="Updated Product",
        barcode="123456789012",
        price_per_unit=15.0,
        note="Updated note",
        quantity=100,
        position="1-A-2"
    )
    service.repo.update_product.return_value = updated_product

    result = await service.update_product(1, dto)

    service.repo.update_product.assert_awaited_once_with(1, dto)
    assert result.description == "Updated Product"
    assert result.price_per_unit == 15.0


@pytest.mark.asyncio
async def test_update_product_barcode_with_active_sales_raises(service):
    dto = SimpleNamespace(
        description=None,
        barcode="999999999999",
        price_per_unit=None,
        note=None,
        quantity=None,
        position=None
    )

    existing_product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = existing_product
    service.repo.has_active_sales.return_value = True

    with pytest.raises(ConflictError):
        await service.update_product(1, dto)

    service.repo.update_product.assert_not_called()


@pytest.mark.asyncio
async def test_update_product_invalid_new_barcode_raises(service):
    dto = SimpleNamespace(
        description=None,
        barcode="123",
        price_per_unit=None,
        note=None,
        quantity=None,
        position=None
    )

    existing_product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = existing_product

    with pytest.raises(BadRequestError):
        await service.update_product(1, dto)

    service.repo.update_product.assert_not_called()


@pytest.mark.asyncio
async def test_delete_product_invalid_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.delete_product(-1)


@pytest.mark.asyncio
async def test_delete_product_ok(service):
    product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = product
    service.repo.has_active_sales.return_value = False
    service.repo.has_active_orders.return_value = False
    service.repo.has_active_returns.return_value = False
    service.repo.delete_product.return_value = True

    result = await service.delete_product(1)

    service.repo.delete_product.assert_awaited_once_with(1)
    assert result is True


@pytest.mark.asyncio
async def test_delete_product_with_active_sales_raises(service):
    product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = product
    service.repo.has_active_sales.return_value = True
    service.repo.has_active_orders.return_value = False
    service.repo.has_active_returns.return_value = False

    with pytest.raises(ConflictError):
        await service.delete_product(1)

    service.repo.delete_product.assert_not_called()


@pytest.mark.asyncio
async def test_delete_product_with_active_orders_raises(service):
    product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = product
    service.repo.has_active_sales.return_value = False
    service.repo.has_active_orders.return_value = True
    service.repo.has_active_returns.return_value = False

    with pytest.raises(ConflictError):
        await service.delete_product(1)

    service.repo.delete_product.assert_not_called()


@pytest.mark.asyncio
async def test_delete_product_with_active_returns_raises(service):
    product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = product
    service.repo.has_active_sales.return_value = False
    service.repo.has_active_orders.return_value = False
    service.repo.has_active_returns.return_value = True

    with pytest.raises(ConflictError):
        await service.delete_product(1)

    service.repo.delete_product.assert_not_called()


@pytest.mark.asyncio
async def test_delete_product_with_multiple_conflicts_raises(service):
    product = SimpleNamespace(id=1, barcode="123456789012")
    service._get_product.return_value = product
    service.repo.has_active_sales.return_value = True
    service.repo.has_active_orders.return_value = True
    service.repo.has_active_returns.return_value = True

    with pytest.raises(ConflictError) as exc_info:
        await service.delete_product(1)

    assert "sales" in str(exc_info.value)
    assert "orders" in str(exc_info.value)
    assert "returns" in str(exc_info.value)
    service.repo.delete_product.assert_not_called()


@pytest.mark.asyncio
async def test_get_product_by_barcode_invalid_barcode_raises(service):
    with pytest.raises(BadRequestError):
        await service.get_product_by_barcode("123")


@pytest.mark.asyncio
async def test_get_product_by_barcode_not_found_raises(service):
    service.repo.get_product_by_barcode.return_value = None

    with pytest.raises(NotFoundError):
        await service.get_product_by_barcode("123456789012")


@pytest.mark.asyncio
async def test_get_product_by_barcode_ok(service):
    product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=10.5,
        note=None,
        quantity=100,
        position=None
    )
    service.repo.get_product_by_barcode.return_value = product

    result = await service.get_product_by_barcode("123456789012")

    service.repo.get_product_by_barcode.assert_awaited_once_with("123456789012")
    assert result.barcode == "123456789012"
    assert result.description == "Test Product"


@pytest.mark.asyncio
async def test_search_products_empty_description_raises(service):
    dto = SimpleNamespace(description="")

    with pytest.raises(BadRequestError):
        await service.search_products(dto)

    service.repo.search_products_by_description.assert_not_called()


@pytest.mark.asyncio
async def test_search_products_whitespace_only_raises(service):
    dto = SimpleNamespace(description="   ")

    with pytest.raises(BadRequestError):
        await service.search_products(dto)

    service.repo.search_products_by_description.assert_not_called()


@pytest.mark.asyncio
async def test_search_products_ok(service):
    dto = SimpleNamespace(description="Test")

    products = [
        SimpleNamespace(id=1, description="Test Product 1", barcode="111111111111",
                       price_per_unit=10.0, note=None, quantity=10, position=None),
        SimpleNamespace(id=2, description="Test Product 2", barcode="222222222222",
                       price_per_unit=20.0, note=None, quantity=20, position=None)
    ]
    service.repo.search_products_by_description.return_value = products

    result = await service.search_products(dto)

    service.repo.search_products_by_description.assert_awaited_once_with("Test")
    assert len(result) == 2
    assert result[0].description == "Test Product 1"
    assert result[1].description == "Test Product 2"


@pytest.mark.asyncio
async def test_search_products_no_results(service):
    dto = SimpleNamespace(description="NonExistent")
    service.repo.search_products_by_description.return_value = []

    result = await service.search_products(dto)

    service.repo.search_products_by_description.assert_awaited_once_with("NonExistent")
    assert result == []


@pytest.mark.asyncio
async def test_get_product_invalid_id_raises(service):
    service._get_product.side_effect = BadRequestError("Product ID must be greater than 0")
    
    with pytest.raises(BadRequestError):
        await service.get_product(0)


@pytest.mark.asyncio
async def test_update_product_position_invalid_format_raises(service):
    dto = SimpleNamespace(position="invalid")

    service._get_product.return_value = SimpleNamespace(id=1)

    with pytest.raises(BadRequestError):
        await service.update_product_position(1, dto)

    service.repo.update_product_position.assert_not_called()


@pytest.mark.asyncio
async def test_update_product_position_ok(service):
    dto = SimpleNamespace(position="2-B-3")

    service._get_product.return_value = SimpleNamespace(id=1)
    updated = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=100,
        position="2-B-3"
    )
    service.repo.update_product_position.return_value = updated

    result = await service.update_product_position(1, dto)

    service.repo.update_product_position.assert_awaited_once_with(1, dto)
    assert result.position == "2-B-3"


@pytest.mark.asyncio
async def test_update_product_position_to_null(service):
    dto = SimpleNamespace(position=None)

    service._get_product.return_value = SimpleNamespace(id=1)
    updated = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=100,
        position=None
    )
    service.repo.update_product_position.return_value = updated

    result = await service.update_product_position(1, dto)

    service.repo.update_product_position.assert_awaited_once_with(1, dto)
    assert result.position is None


@pytest.mark.asyncio
async def test_update_product_position_empty_string(service):
    dto = SimpleNamespace(position="")

    service._get_product.return_value = SimpleNamespace(id=1)
    updated = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=100,
        position=""
    )
    service.repo.update_product_position.return_value = updated

    result = await service.update_product_position(1, dto)

    service.repo.update_product_position.assert_awaited_once_with(1, dto)


@pytest.mark.asyncio
async def test_update_product_quantity_invalid_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.update_product_quantity(-1, 10)


@pytest.mark.asyncio
async def test_update_product_quantity_add_ok(service):
    service._get_product.return_value = SimpleNamespace(id=1)
    updated = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=110,
        position=None
    )
    service.repo.update_product_quantity.return_value = updated

    result = await service.update_product_quantity(1, 10)

    service.repo.update_product_quantity.assert_awaited_once_with(1, 10)
    assert result.quantity == 110


@pytest.mark.asyncio
async def test_update_product_quantity_subtract_ok(service):
    service._get_product.return_value = SimpleNamespace(id=1)
    updated = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=10.0,
        note=None,
        quantity=90,
        position=None
    )
    service.repo.update_product_quantity.return_value = updated

    result = await service.update_product_quantity(1, -10)

    service.repo.update_product_quantity.assert_awaited_once_with(1, -10)
    assert result.quantity == 90


@pytest.mark.asyncio
async def test_update_product_quantity_negative_result_raises(service):
    service._get_product.return_value = SimpleNamespace(id=1)
    service.repo.update_product_quantity.side_effect = ValueError("Quantity cannot be negative")

    with pytest.raises(BadRequestError):
        await service.update_product_quantity(1, -200)

    service.repo.update_product_quantity.assert_awaited_once_with(1, -200)