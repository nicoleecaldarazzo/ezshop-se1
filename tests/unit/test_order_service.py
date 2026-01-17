import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.services.order_service import OrderService
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.notfound_error import NotFoundError
from app.models.order_status import OrderStatus


@pytest.fixture
def service():
    s = OrderService()

    s.repo = MagicMock()
    s.repo.create_order = AsyncMock()
    s.repo.list_orders = AsyncMock()
    s.repo.get_order_by_id = AsyncMock()
    s.repo.create_and_pay_order = AsyncMock()
    s.repo.pay_order = AsyncMock()
    s.repo.record_order_arrival = AsyncMock()

    s._get_order = AsyncMock()

    return s


@pytest.mark.asyncio
async def test_create_order_success(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99
    )

    created_order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date="2026-01-03T10:00:00"
    )
    service.repo.create_order.return_value = created_order

    result = await service.create_order(dto)

    service.repo.create_order.assert_awaited_once_with(dto)
    assert result.id == 1
    assert result.product_barcode == "123456789012"
    assert result.quantity == 10
    assert result.price_per_unit == 99.99
    assert result.status == OrderStatus.ISSUED


@pytest.mark.asyncio
async def test_create_order_invalid_barcode_empty_raises(service):
    dto = SimpleNamespace(
        product_barcode="",
        quantity=10,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Barcode must be a string of 12-14 digits"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_invalid_barcode_whitespace_raises(service):
    dto = SimpleNamespace(
        product_barcode="   ",
        quantity=10,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Barcode must be a string of 12-14 digits"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_invalid_barcode_format_raises(service):
    dto = SimpleNamespace(
        product_barcode="123",
        quantity=10,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Barcode must be a string of 12-14 digits"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_invalid_barcode_non_numeric_raises(service):
    dto = SimpleNamespace(
        product_barcode="ABC123456789",
        quantity=10,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Barcode must be a string of 12-14 digits"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_zero_quantity_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=0,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Quantity must be greater than 0"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_negative_quantity_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=-5,
        price_per_unit=99.99
    )

    with pytest.raises(BadRequestError, match="Quantity must be greater than 0"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_zero_price_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=0.0
    )

    with pytest.raises(BadRequestError, match="Price per unit must be greater than 0"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_negative_price_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=-10.5
    )

    with pytest.raises(BadRequestError, match="Price per unit must be greater than 0"):
        await service.create_order(dto)

    service.repo.create_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_product_not_found_raises(service):
    dto = SimpleNamespace(
        product_barcode="614141007349",
        quantity=10,
        price_per_unit=99.99
    )

    service.repo.create_order.side_effect = ValueError("Product not found")

    with pytest.raises(NotFoundError, match="Product not found"):
        await service.create_order(dto)

    service.repo.create_order.assert_awaited_once_with(dto)


@pytest.mark.asyncio
async def test_create_order_repo_returns_none_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99
    )

    service.repo.create_order.return_value = None

    with pytest.raises(Exception, match="Failed to create order"):
        await service.create_order(dto)


@pytest.mark.asyncio
async def test_list_orders_success(service):
    orders = [
        SimpleNamespace(
            id=1,
            product_barcode="123456789012",
            quantity=10,
            price_per_unit=99.99,
            status=OrderStatus.ISSUED,
            issue_date="2026-01-03T10:00:00"
        ),
        SimpleNamespace(
            id=2,
            product_barcode="987654321098",
            quantity=5,
            price_per_unit=49.99,
            status=OrderStatus.PAID,
            issue_date="2026-01-03T11:00:00"
        )
    ]
    service.repo.list_orders.return_value = orders

    result = await service.list_orders()

    service.repo.list_orders.assert_awaited_once()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


@pytest.mark.asyncio
async def test_list_orders_empty(service):
    service.repo.list_orders.return_value = []

    result = await service.list_orders()

    service.repo.list_orders.assert_awaited_once()
    assert result == []


@pytest.mark.asyncio
async def test_create_and_pay_order_success(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=20
    )

    created_order = SimpleNamespace(
        id=3,
        product_barcode="123456789012",
        quantity=20,
        price_per_unit=79.99,
        status=OrderStatus.PAID,
        issue_date="2026-01-03T12:00:00"
    )
    service.repo.create_and_pay_order.return_value = created_order

    result = await service.create_and_pay_order(dto)

    service.repo.create_and_pay_order.assert_awaited_once_with(dto)
    assert result.id == 3
    assert result.status == OrderStatus.PAID
    assert result.price_per_unit == 79.99


@pytest.mark.asyncio
async def test_create_and_pay_order_invalid_barcode_raises(service):
    dto = SimpleNamespace(
        product_barcode="",
        quantity=20
    )

    with pytest.raises(BadRequestError, match="Barcode must be a string of 12-14 digits"):
        await service.create_and_pay_order(dto)

    service.repo.create_and_pay_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_and_pay_order_invalid_quantity_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=0
    )

    with pytest.raises(BadRequestError, match="Quantity must be greater than 0"):
        await service.create_and_pay_order(dto)

    service.repo.create_and_pay_order.assert_not_called()


@pytest.mark.asyncio
async def test_create_and_pay_order_product_not_found_raises(service):
    dto = SimpleNamespace(
        product_barcode="614141007349",
        quantity=20
    )

    service.repo.create_and_pay_order.side_effect = ValueError("Product not found")

    with pytest.raises(NotFoundError, match="Product not found"):
        await service.create_and_pay_order(dto)


@pytest.mark.asyncio
async def test_create_and_pay_order_repo_returns_none_raises(service):
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=20
    )

    service.repo.create_and_pay_order.return_value = None

    with pytest.raises(Exception, match="Failed to create and pay order"):
        await service.create_and_pay_order(dto)


@pytest.mark.asyncio
async def test_pay_order_success(service):
    payment_dto = SimpleNamespace()
    
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date="2026-01-03T10:00:00"
    )
    service._get_order.return_value = order

    updated_order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.PAID,
        issue_date="2026-01-03T10:00:00"
    )
    service.repo.pay_order.return_value = updated_order

    result = await service.pay_order(1, payment_dto)

    service._get_order.assert_awaited_once_with(1)
    service.repo.pay_order.assert_awaited_once_with(1)
    assert result.id == 1
    assert result.status == OrderStatus.PAID


@pytest.mark.asyncio
async def test_pay_order_invalid_id_raises(service):
    payment_dto = SimpleNamespace()

    service._get_order.side_effect = BadRequestError("Order ID must be greater than 0")

    with pytest.raises(BadRequestError, match="Order ID must be greater than 0"):
        await service.pay_order(0, payment_dto)

    service.repo.pay_order.assert_not_called()


@pytest.mark.asyncio
async def test_pay_order_not_found_raises(service):
    payment_dto = SimpleNamespace()

    service._get_order.side_effect = NotFoundError("Order with id '999' not found")

    with pytest.raises(NotFoundError, match="Order with id '999' not found"):
        await service.pay_order(999, payment_dto)

    service.repo.pay_order.assert_not_called()


@pytest.mark.asyncio
async def test_pay_order_wrong_status_raises(service):
    payment_dto = SimpleNamespace()
    
    order = SimpleNamespace(id=1)
    service._get_order.return_value = order

    service.repo.pay_order.side_effect = ConflictError(
        "Order must be in ISSUED state to be paid (current: COMPLETED)"
    )

    with pytest.raises(ConflictError, match="Order must be in ISSUED state"):
        await service.pay_order(1, payment_dto)

    service._get_order.assert_awaited_once_with(1)
    service.repo.pay_order.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_pay_order_repo_returns_none_raises(service):
    payment_dto = SimpleNamespace()
    
    order = SimpleNamespace(id=1)
    service._get_order.return_value = order

    service.repo.pay_order.return_value = None

    with pytest.raises(NotFoundError, match="Order with id '1' not found"):
        await service.pay_order(1, payment_dto)


@pytest.mark.asyncio
async def test_record_order_arrival_success(service):
    arrival_dto = SimpleNamespace()
    
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.PAID,
        issue_date="2026-01-03T10:00:00"
    )
    service._get_order.return_value = order

    completed_order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.COMPLETED,
        issue_date="2026-01-03T10:00:00"
    )
    service.repo.record_order_arrival.return_value = completed_order

    result = await service.record_order_arrival(1, arrival_dto)

    service._get_order.assert_awaited_once_with(1)
    service.repo.record_order_arrival.assert_awaited_once_with(1)
    assert result.id == 1
    assert result.status == OrderStatus.COMPLETED


@pytest.mark.asyncio
async def test_record_order_arrival_invalid_id_raises(service):
    arrival_dto = SimpleNamespace()

    service._get_order.side_effect = BadRequestError("Order ID must be greater than 0")

    with pytest.raises(BadRequestError, match="Order ID must be greater than 0"):
        await service.record_order_arrival(0, arrival_dto)

    service.repo.record_order_arrival.assert_not_called()


@pytest.mark.asyncio
async def test_record_order_arrival_not_found_raises(service):
    arrival_dto = SimpleNamespace()

    service._get_order.side_effect = NotFoundError("Order with id '999' not found")

    with pytest.raises(NotFoundError, match="Order with id '999' not found"):
        await service.record_order_arrival(999, arrival_dto)

    service.repo.record_order_arrival.assert_not_called()


@pytest.mark.asyncio
async def test_record_order_arrival_wrong_status_raises(service):
    arrival_dto = SimpleNamespace()
    
    order = SimpleNamespace(id=1)
    service._get_order.return_value = order

    service.repo.record_order_arrival.side_effect = ConflictError(
        "Order must be in PAID state to record arrival (current: ISSUED)"
    )

    with pytest.raises(ConflictError, match="Order must be in PAID state"):
        await service.record_order_arrival(1, arrival_dto)

    service._get_order.assert_awaited_once_with(1)
    service.repo.record_order_arrival.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_record_order_arrival_product_not_found_raises(service):
    arrival_dto = SimpleNamespace()
    
    order = SimpleNamespace(id=1)
    service._get_order.return_value = order

    service.repo.record_order_arrival.side_effect = ValueError("Product not found")

    with pytest.raises(NotFoundError, match="Product not found"):
        await service.record_order_arrival(1, arrival_dto)


@pytest.mark.asyncio
async def test_record_order_arrival_repo_returns_none_raises(service):
    arrival_dto = SimpleNamespace()
    
    order = SimpleNamespace(id=1)
    service._get_order.return_value = order

    service.repo.record_order_arrival.return_value = None

    with pytest.raises(NotFoundError, match="Order with id '1' not found"):
        await service.record_order_arrival(1, arrival_dto)


@pytest.mark.asyncio
async def test_get_order_helper_invalid_id_raises(service):
    service._get_order = OrderService._get_order.__get__(service, OrderService)
    
    with pytest.raises(BadRequestError, match="Order ID must be greater than 0"):
        await service._get_order(0)


@pytest.mark.asyncio
async def test_get_order_helper_negative_id_raises(service):
    service._get_order = OrderService._get_order.__get__(service, OrderService)
    
    with pytest.raises(BadRequestError, match="Order ID must be greater than 0"):
        await service._get_order(-5)


@pytest.mark.asyncio
async def test_get_order_helper_not_found_raises(service):
    service._get_order = OrderService._get_order.__get__(service, OrderService)
    service.repo.get_order_by_id.return_value = None
    
    with pytest.raises(NotFoundError, match="Order with id '999' not found"):
        await service._get_order(999)


@pytest.mark.asyncio
async def test_get_order_helper_success(service):
    service._get_order = OrderService._get_order.__get__(service, OrderService)
    
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date="2026-01-03T10:00:00"
    )
    service.repo.get_order_by_id.return_value = order
    
    result = await service._get_order(1)
    
    assert result.id == 1
    assert result.product_barcode == "123456789012"