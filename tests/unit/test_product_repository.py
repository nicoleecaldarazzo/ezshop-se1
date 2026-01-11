import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace

from app.repositories.product_repository import ProductRepository
from app.models.errors.conflict_error import ConflictError


@pytest.fixture
def repo():
    r = ProductRepository()
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
async def test_create_product_success(repo, mock_session):
    mock_barcode_result = MagicMock()
    mock_barcode_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_barcode_result)
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="Lipstick",
        barcode="123456789012",
        price_per_unit=9.99,
        note="Red lipstick",
        quantity=100,
        position="1-A-2"
    )
    
    result = await repo.create_product(dto)
    
    mock_session.execute.assert_awaited_once()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_product_duplicate_barcode_raises(repo, mock_session):
    existing_product = SimpleNamespace(barcode="123456789012")
    mock_barcode_result = MagicMock()
    mock_barcode_result.scalar_one_or_none.return_value = existing_product
    mock_session.execute = AsyncMock(return_value=mock_barcode_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="Lipstick",
        barcode="123456789012",
        price_per_unit=9.99,
        note=None,
        quantity=10,
        position=None
    )
    
    with pytest.raises(ConflictError, match="Product barcode already exists"):
        await repo.create_product(dto)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_sets_all_fields(repo, mock_session):
    mock_barcode_result = MagicMock()
    mock_barcode_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_barcode_result)
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="Test Product",
        barcode="123456789012",
        price_per_unit=49.99,
        note="Important note",
        quantity=50,
        position="2-B-3"
    )
    
    await repo.create_product(dto)
    
    call_args = mock_session.add.call_args[0][0]
    assert call_args.description == "Test Product"
    assert call_args.barcode == "123456789012"
    assert call_args.price_per_unit == 49.99
    assert call_args.note == "Important note"
    assert call_args.quantity == 50
    assert call_args.position == "2-B-3"


@pytest.mark.asyncio
async def test_list_products_success(repo, mock_session):
    product1 = SimpleNamespace(
        id=1,
        description="Product 1",
        barcode="111111111111",
        price_per_unit=10.00,
        note=None,
        quantity=100,
        position="1-A-1"
    )
    product2 = SimpleNamespace(
        id=2,
        description="Product 2",
        barcode="222222222222",
        price_per_unit=20.00,
        note="Note 2",
        quantity=50,
        position=None
    )
    
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [product1, product2]
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.list_products()
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_products_empty(repo, mock_session):
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.list_products()
    
    assert result == []
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_product_by_id_found(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=99.99,
        note="Test note",
        quantity=100,
        position="1-A-2"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_product_by_id(1)
    
    assert result.id == 1
    assert result.description == "Test Product"
    assert result.barcode == "123456789012"
    mock_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_product_by_id(999)
    
    assert result is None
    mock_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_product_by_barcode_found(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012",
        price_per_unit=99.99,
        note=None,
        quantity=100,
        position=None
    )
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = product
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_product_by_barcode("123456789012")
    
    assert result.barcode == "123456789012"
    assert result.description == "Test Product"
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_product_by_barcode_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.get_product_by_barcode("999999999999")
    
    assert result is None
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_search_products_by_description_found(repo, mock_session):
    product1 = SimpleNamespace(
        id=1,
        description="Laptop Computer",
        barcode="111111111111",
        price_per_unit=999.99,
        note=None,
        quantity=10,
        position="1-A-1"
    )
    product2 = SimpleNamespace(
        id=2,
        description="Desktop Computer",
        barcode="222222222222",
        price_per_unit=1299.99,
        note=None,
        quantity=5,
        position="1-A-2"
    )
    
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [product1, product2]
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.search_products_by_description("Computer")
    
    assert len(result) == 2
    assert "Computer" in result[0].description
    assert "Computer" in result[1].description
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_search_products_by_description_no_results(repo, mock_session):
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute = AsyncMock(return_value=mock_result)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.search_products_by_description("NonExistent")
    
    assert result == []
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_success(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Old Description",
        barcode="123456789012",
        price_per_unit=50.00,
        note="Old note",
        quantity=100,
        position="1-A-1"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="New Description",
        barcode=None,
        price_per_unit=75.00,
        note="New note",
        quantity=None,
        position=None
    )
    
    result = await repo.update_product(1, dto)
    
    assert product.description == "New Description"
    assert product.price_per_unit == 75.00
    assert product.note == "New note"
    assert product.barcode == "123456789012"
    mock_session.get.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_not_found_returns_none(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="New",
        barcode=None,
        price_per_unit=None,
        note=None,
        quantity=None,
        position=None
    )
    
    result = await repo.update_product(999, dto)
    
    assert result is None
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_barcode_conflict_raises(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        barcode="123456789012"
    )
    
    existing_product = SimpleNamespace(barcode="999999999999")
    mock_barcode_result = MagicMock()
    mock_barcode_result.scalar_one_or_none.return_value = existing_product
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.execute = AsyncMock(return_value=mock_barcode_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description=None,
        barcode="999999999999",
        price_per_unit=None,
        note=None,
        quantity=None,
        position=None
    )
    
    with pytest.raises(ConflictError, match="Barcode already exists"):
        await repo.update_product(1, dto)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_same_barcode_allowed(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=50.00,
        note=None,
        quantity=100,
        position=None
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description="Updated",
        barcode="123456789012",
        price_per_unit=None,
        note=None,
        quantity=None,
        position=None
    )
    
    result = await repo.update_product(1, dto)
    
    assert product.description == "Updated"
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_partial_update(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Original",
        barcode="123456789012",
        price_per_unit=50.00,
        note="Original note",
        quantity=100,
        position="1-A-1"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(
        description=None,
        barcode=None,
        price_per_unit=75.00,
        note=None,
        quantity=None,
        position="2-B-2"
    )
    
    await repo.update_product(1, dto)
    
    assert product.price_per_unit == 75.00
    assert product.position == "2-B-2"
    assert product.description == "Original"
    assert product.barcode == "123456789012"
    assert product.note == "Original note"
    assert product.quantity == 100


@pytest.mark.asyncio
async def test_delete_product_success(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test Product",
        barcode="123456789012"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.delete_product(1)
    
    assert result is True
    mock_session.get.assert_awaited_once()
    mock_session.delete.assert_awaited_once_with(product)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_product_not_found_returns_false(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.delete_product(999)
    
    assert result is False
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_position_success(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=50.00,
        note=None,
        quantity=100,
        position="1-A-1"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(position="2-B-3")
    
    result = await repo.update_product_position(1, dto)
    
    assert product.position == "2-B-3"
    mock_session.get.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_position_not_found_returns_none(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(position="2-B-3")
    
    result = await repo.update_product_position(999, dto)
    
    assert result is None
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_position_to_none(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        position="1-A-1"
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    dto = SimpleNamespace(position=None)
    
    await repo.update_product_position(1, dto)
    
    assert product.position is None
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_quantity_add_success(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        description="Test",
        barcode="123456789012",
        price_per_unit=50.00,
        note=None,
        quantity=100,
        position=None
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.update_product_quantity(1, 50)
    
    assert product.quantity == 150
    mock_session.get.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_quantity_subtract_success(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        quantity=100
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.update_product_quantity(1, -30)
    
    assert product.quantity == 70
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_product_quantity_not_found_returns_none(repo, mock_session):
    mock_session.get = AsyncMock(return_value=None)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.update_product_quantity(999, 10)
    
    assert result is None
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_quantity_negative_result_raises(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        quantity=50
    )
    
    mock_session.get = AsyncMock(return_value=product)
    repo._get_session = AsyncMock(return_value=mock_session)
    
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        await repo.update_product_quantity(1, -100)
    
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_product_quantity_to_zero(repo, mock_session):
    product = SimpleNamespace(
        id=1,
        quantity=50
    )
    
    mock_session.get = AsyncMock(return_value=product)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.update_product_quantity(1, -50)
    
    assert product.quantity == 0
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_sales_true(repo, mock_session):
    sale_line = SimpleNamespace(product_barcode="123456789012")
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sale_line
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_sales("123456789012")
    
    assert result is True
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_sales_false(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_sales("123456789012")
    
    assert result is False
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_orders_true(repo, mock_session):
    order = SimpleNamespace(product_barcode="123456789012")
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = order
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_orders("123456789012")
    
    assert result is True
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_orders_false(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_orders("123456789012")
    
    assert result is False
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_returns_true(repo, mock_session):
    return_line = SimpleNamespace(product_barcode="123456789012")
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = return_line
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_returns("123456789012")
    
    assert result is True
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_has_active_returns_false(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.has_active_returns("123456789012")
    
    assert result is False
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_session_returns_existing_session(repo):
    mock_existing_session = AsyncMock()
    repo._session = mock_existing_session
    
    result = await repo._get_session()
    
    assert result == mock_existing_session


@pytest.mark.asyncio
async def test_get_session_creates_new_session_if_none():
    repo = ProductRepository(session=None)
    
    with patch('app.repositories.product_repository.AsyncSessionLocal') as mock_session_local:
        mock_new_session = AsyncMock()
        mock_session_local.return_value = mock_new_session
        
        result = await repo._get_session()
        
        mock_session_local.assert_called_once()
        assert result == mock_new_session

@pytest.mark.asyncio
async def test_update_product_quantity_field(repo, mock_session):
    product = SimpleNamespace(id=1, quantity=10, barcode="124567890123")
    mock_session.get = AsyncMock(return_value=product)
    
    repo._get_session = AsyncMock(return_value=mock_session)

    dto = SimpleNamespace(
        description=None,
        barcode=None,
        price_per_unit=None,
        note=None,
        quantity=50, 
        position=None
    )

    await repo.update_product(1, dto)

    assert product.quantity == 50