import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace
from datetime import datetime, timezone
from  app.models.errors.invalid_state_error import InvalidStateError
from app.repositories.order_repository import OrderRepository
from app.models.order_status import OrderStatus


@pytest.fixture
def repo():
    r = OrderRepository()
    
    mock_session = AsyncMock()
    r._session = mock_session
    
    return r


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.mark.asyncio
async def test_create_order_success(repo, mock_session):
    mock_product = SimpleNamespace(
        barcode="123456789012",
        price_per_unit=99.99,
        quantity=100
    )

    mock_system_info = SimpleNamespace(
        balance=2000.0  
    )

    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = mock_product

    mock_balance_result = MagicMock()
    mock_balance_result.scalar_one_or_none.return_value = mock_system_info
    
    mock_session.execute = AsyncMock(side_effect=[mock_product_result, mock_balance_result])
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99
    )
    
    result = await repo.create_and_pay_order(dto)
    
    assert mock_session.execute.await_count == 2
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_order_product_not_found_raises(repo, mock_session):
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="999999999999",
        quantity=10,
        price_per_unit=99.99
    )
    
    with pytest.raises(ValueError, match="Product not found"):
        await repo.create_order(dto)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_order_sets_issued_status(repo, mock_session):
    mock_product = SimpleNamespace(barcode="123456789012")
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = mock_product
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99
    )
    
    await repo.create_order(dto)
    
    call_args = mock_session.add.call_args[0][0]
    assert call_args.status == OrderStatus.ISSUED
    assert call_args.product_barcode == "123456789012"
    assert call_args.quantity == 10
    assert call_args.price_per_unit == 99.99


@pytest.mark.asyncio
async def test_list_orders_success(repo, mock_session):
    order1 = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date=datetime.now(timezone.utc)
    )
    order2 = SimpleNamespace(
        id=2,
        product_barcode="987654321098",
        quantity=5,
        price_per_unit=49.99,
        status=OrderStatus.PAID,
        issue_date=datetime.now(timezone.utc)
    )
    
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [order1, order2]
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.list_orders()
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_orders_empty(repo, mock_session):
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.list_orders()
    
    assert result == []
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_order_by_id_found(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date=datetime.now(timezone.utc)
    )
    
    mock_session.get = AsyncMock(return_value=order)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_order_by_id(1)
    
    assert result.id == 1
    assert result.product_barcode == "123456789012"
    mock_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_order_by_id_not_found(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_order_by_id(999)
    
    assert result is None
    mock_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_and_pay_order_success(repo, mock_session):
    mock_product = SimpleNamespace(
        barcode="123456789012",
        price_per_unit=79.99,
        quantity=100
    )

    mock_system_info = SimpleNamespace(
        balance=2000.0  
    )
    
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = mock_product
    
    mock_balance_result = MagicMock()
    mock_balance_result.scalar_one_or_none.return_value = mock_system_info
    
    mock_session.execute = AsyncMock(side_effect=[mock_product_result, mock_balance_result])
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=20
    )
    
    result = await repo.create_and_pay_order(dto)
    
    assert mock_session.execute.await_count == 2
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_and_pay_order_uses_product_price(repo, mock_session):
    mock_product = SimpleNamespace(
        barcode="123456789012",
        price_per_unit=79.99
    )

    mock_system_info = SimpleNamespace(
        balance=2000.0
    )

    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = mock_product
    mock_balance_result = MagicMock()
    mock_balance_result.scalar_one_or_none.return_value = mock_system_info
    mock_session.execute = AsyncMock(side_effect=[mock_product_result, mock_balance_result])
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="123456789012",
        quantity=20
    )
    
    await repo.create_and_pay_order(dto)
    
    call_args = mock_session.add.call_args[0][0]
    assert call_args.price_per_unit == 79.99
    assert call_args.status == OrderStatus.PAID


@pytest.mark.asyncio
async def test_create_and_pay_order_product_not_found_raises(repo, mock_session):
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        product_barcode="999999999999",
        quantity=20
    )
    
    with pytest.raises(ValueError, match="Product not found"):
        await repo.create_and_pay_order(dto)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_pay_order_success(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        price_per_unit=99.99,
        status=OrderStatus.ISSUED,
        issue_date=datetime.now(timezone.utc)
    )
    
    mock_session.get = AsyncMock(return_value=order)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.pay_order(1)
    
    assert order.status == OrderStatus.PAID
    mock_session.get.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_pay_order_not_found_returns_none(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.pay_order(999)
    
    assert result is None
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_pay_order_not_issued_raises_conflict(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        status=OrderStatus.PAID
    )
    
    mock_session.get = AsyncMock(return_value=order)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(InvalidStateError, match="Order must be in ISSUED state"):
        await repo.pay_order(1)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_pay_order_completed_raises_conflict(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        status=OrderStatus.COMPLETED
    )
    
    mock_session.get = AsyncMock(return_value=order)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(InvalidStateError, match="Order must be in ISSUED state"):
        await repo.pay_order(1)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_record_order_arrival_success(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=10,
        status=OrderStatus.PAID
    )
    
    product = SimpleNamespace(
        barcode="123456789012",
        quantity=50,
        position="1-A-1"
    )
    
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = product
    
    mock_session.get = AsyncMock(return_value=order)
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.record_order_arrival(1)
    
    assert order.status == OrderStatus.COMPLETED
    assert product.quantity == 60
    
    mock_session.get.assert_awaited_once()
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert mock_session.refresh.await_count == 2


@pytest.mark.asyncio
async def test_record_order_arrival_order_not_found_returns_none(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.record_order_arrival(999)
    
    assert result is None
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_record_order_arrival_not_paid_raises_conflict(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        status=OrderStatus.ISSUED
    )
    
    mock_session.get = AsyncMock(return_value=order)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(InvalidStateError, match="Order must be in PAID state"):
        await repo.record_order_arrival(1)
    
    mock_session.execute.assert_not_awaited()
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_record_order_arrival_already_completed_raises_conflict(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        status=OrderStatus.COMPLETED
    )
    
    mock_session.get = AsyncMock(return_value=order)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(InvalidStateError, match="Order must be in PAID state"):
        await repo.record_order_arrival(1)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_record_order_arrival_product_not_found_raises(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        product_barcode="999999999999",
        quantity=10,
        status=OrderStatus.PAID
    )
    
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = None
    
    mock_session.get = AsyncMock(return_value=order)
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(ValueError, match="Product not found"):
        await repo.record_order_arrival(1)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_record_order_arrival_updates_product_quantity_correctly(repo, mock_session):
    order = SimpleNamespace(
        id=1,
        product_barcode="123456789012",
        quantity=25,
        status=OrderStatus.PAID
    )
    
    product = SimpleNamespace(
        barcode="123456789012",
        quantity=100,
        position="1-A-1"
    )
    
    mock_product_result = MagicMock()
    mock_product_result.scalar_one_or_none.return_value = product
    
    mock_session.get = AsyncMock(return_value=order)
    mock_session.execute = AsyncMock(return_value=mock_product_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    await repo.record_order_arrival(1)
    
    assert product.quantity == 125


@pytest.mark.asyncio
async def test_get_session_returns_existing_session(repo):
    mock_existing_session = AsyncMock()
    repo._session = mock_existing_session
    
    result = await repo._get_session()
    
    assert result == mock_existing_session


@pytest.mark.asyncio
async def test_get_session_creates_new_session_if_none():
    repo = OrderRepository(session=None)
    
    with patch('app.repositories.order_repository.AsyncSessionLocal') as mock_session_local:
        mock_new_session = AsyncMock()
        mock_session_local.return_value = mock_new_session
        
        result = await repo._get_session()
        
        mock_session_local.assert_called_once()
        assert result == mock_new_session