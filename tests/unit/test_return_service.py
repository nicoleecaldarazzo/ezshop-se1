import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.return_service import ReturnService
from app.models.return_status import ReturnStatus
from app.models.errors.conflict_error import ConflictError

@pytest.mark.asyncio
async def test_create_return_success():
    """Test creating a return successfully when sale is PAID."""
    service = ReturnService()
    
    # Mock Sale Repo to return a 'PAID' sale
    mock_sale = MagicMock()
    mock_sale.status = "PAID"
    service.sale_repo.get_sale = AsyncMock(return_value=mock_sale)

    # Mock Return Repo to return the created object
    mock_return = MagicMock()
    mock_return.id = 1
    mock_return.status = ReturnStatus.OPEN
    service.repo.create_return = AsyncMock(return_value=mock_return)

    result = await service.create_return(sale_id=10)

    assert result.id == 1
    assert result.status == ReturnStatus.OPEN

@pytest.mark.asyncio
async def test_create_return_fails_if_unpaid():
    """Test that creating a return fails if the sale is not PAID."""
    service = ReturnService()
    
    # Mock Sale Repo to return an 'OPEN' (unpaid) sale
    mock_sale = MagicMock()
    mock_sale.status = "OPEN"
    service.sale_repo.get_sale = AsyncMock(return_value=mock_sale)

    # Action & Assert: Expect ConflictError
    with pytest.raises(ConflictError):
        await service.create_return(sale_id=10)

@pytest.mark.asyncio
async def test_close_return_restocks_items():
    """Test that closing a return puts items back into inventory."""
    service = ReturnService()
    
    # Mock a Return that has 1 line item (5 units of Product 'ABC')
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.OPEN
    
    line_item = MagicMock()
    line_item.product_barcode = "ABC"
    line_item.quantity = 5
    mock_ret.lines = [line_item]
    
    service.repo.get_return = AsyncMock(return_value=mock_ret)
    service.repo.close_return = AsyncMock(return_value=True)
    
    # Mock Product Repository
    # The service will look up the product by barcode to get its ID
    mock_product = MagicMock()
    mock_product.id = 99
    service.product_repo.get_product_by_barcode = AsyncMock(return_value=mock_product)
    service.product_repo.update_product_quantity = AsyncMock()

    await service.close_return(return_id=1)

    service.product_repo.get_product_by_barcode.assert_called_with("ABC")
    service.product_repo.update_product_quantity.assert_called_with(99, 5)
