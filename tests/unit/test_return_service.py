import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from app.services.return_service import ReturnService
from app.models.return_status import ReturnStatus
from app.models.errors.conflict_error import ConflictError
from app.models.errors.notfound_error import NotFoundError


@pytest.mark.asyncio
async def test_create_return_success():
    service = ReturnService()
    
    # Mock Sale (PAID)
    mock_sale = MagicMock()
    mock_sale.status = "PAID"
    service.sale_repo.get_sale = AsyncMock(return_value=mock_sale)

    # Mock DAO Return
    mock_dao = MagicMock()
    mock_dao.id = 1
    mock_dao.status = ReturnStatus.OPEN
    mock_dao.lines = []
    service.repo.create_return = AsyncMock(return_value=mock_dao)

    result = await service.create_return(sale_id=10)
    assert result.id == 1
    assert result.status == ReturnStatus.OPEN

@pytest.mark.asyncio
async def test_create_return_fails_if_unpaid():
    service = ReturnService()
    mock_sale = MagicMock()
    mock_sale.status = "OPEN" # Not paid
    service.sale_repo.get_sale = AsyncMock(return_value=mock_sale)

    with pytest.raises(ConflictError):
        await service.create_return(sale_id=10)

@pytest.mark.asyncio
async def test_get_return_not_found():
    service = ReturnService()
    service.repo.get_return = AsyncMock(return_value=None)
    
    with pytest.raises(NotFoundError):
        await service.get_return(999)

@pytest.mark.asyncio
async def test_delete_return_reimbursed_conflict():
    service = ReturnService()
    mock_dao = MagicMock()
    mock_dao.status = ReturnStatus.REIMBURSED
    service.repo.get_return = AsyncMock(return_value=mock_dao)
    
    with pytest.raises(ConflictError):
        await service.delete_return(1)

@pytest.mark.asyncio
async def test_delete_return_success():
    service = ReturnService()
    mock_dao = MagicMock()
    mock_dao.status = ReturnStatus.OPEN
    service.repo.get_return = AsyncMock(return_value=mock_dao)
    service.repo.delete_return = AsyncMock(return_value=True)

    result = await service.delete_return(1)
    assert result is True

@pytest.mark.asyncio
async def test_add_item_closed_conflict():
    service = ReturnService()
    mock_dao = MagicMock()
    mock_dao.status = ReturnStatus.CLOSED
    service.repo.get_return = AsyncMock(return_value=mock_dao)

    with pytest.raises(ConflictError):
        await service.add_item(1, "ABC", 1)

@pytest.mark.asyncio
async def test_remove_item_closed_conflict():
    service = ReturnService()
    mock_dao = MagicMock()
    mock_dao.status = ReturnStatus.CLOSED
    service.repo.get_return = AsyncMock(return_value=mock_dao)

    with pytest.raises(ConflictError):
        await service.remove_item(1, "ABC", 1)

@pytest.mark.asyncio
async def test_close_return_restocks_items():
    service = ReturnService()
    
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.OPEN
    
    line_item = MagicMock()
    line_item.product_barcode = "ABC"
    line_item.quantity = 5
    mock_ret.lines = [line_item]
    
    service.repo.get_return = AsyncMock(return_value=mock_ret)
    service.repo.close_return = AsyncMock(return_value=True)
    
    # Mock Product lookup
    mock_prod = MagicMock()
    mock_prod.id = 99
    service.product_repo.get_product_by_barcode = AsyncMock(return_value=mock_prod)
    service.product_repo.update_product_quantity = AsyncMock()

    await service.close_return(return_id=1)

    service.product_repo.update_product_quantity.assert_called_with(99, 5)

@pytest.mark.asyncio
async def test_reimburse_return_success():
    service = ReturnService()
    
    # Mock a closed return
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.CLOSED
    # 2 items @ 10.00 each = 20.00 refund
    line = MagicMock()
    line.quantity = 2
    line.price_per_unit = 10.0
    mock_ret.lines = [line]
    
    service.repo.get_return = AsyncMock(return_value=mock_ret)
    service.accounting_repo.update_balance = AsyncMock()
    service.repo.reimburse_return = AsyncMock()

    result = await service.reimburse_return(1)

    assert result["refund_amount"] == 20.0
    # Ensure balance was deducted (negative value)
    service.accounting_repo.update_balance.assert_awaited_once_with(-20.0)

@pytest.mark.asyncio
async def test_reimburse_return_not_closed_conflict():
    service = ReturnService()
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.OPEN
    service.repo.get_return = AsyncMock(return_value=mock_ret)

    with pytest.raises(ConflictError):
        await service.reimburse_return(1)