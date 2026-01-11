import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from types import SimpleNamespace

from app.services.sale_service import SaleService
from app.models.sale_status import SaleStatus
from app.models.DTO.boolean_response_dto import BooleanResponseDTO
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.invalid_state_error import InvalidStateError


@pytest.fixture
def service():
    s = SaleService()
    s.repo = AsyncMock()
    return s

@pytest.mark.asyncio
async def test_create_sale(service):
    service.repo.create_sale.return_value = SimpleNamespace(id=1)
    result = await service.create_sale()
    assert result.id == 1
    service.repo.create_sale.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_sale_success(service):
    service.repo.get_sale.return_value = SimpleNamespace(id=1)
    result = await service.get_sale(1)
    assert result.id == 1

@pytest.mark.asyncio
async def test_get_sale_not_found(service):
    service.repo.get_sale.return_value = None
    with pytest.raises(NotFoundError):
        await service.get_sale(999)

@pytest.mark.asyncio
async def test_add_item_success(service):
    # Sale must be OPEN
    sale = SimpleNamespace(id=1, status=SaleStatus.OPEN)
    service.repo.get_sale.return_value = sale
    service.repo.add_line.return_value = True

    result = await service.add_item(1, "ABC", 2)
    
    assert isinstance(result, BooleanResponseDTO)
    assert result.success is True
    service.repo.add_line.assert_awaited_once_with(1, "ABC", 2)

@pytest.mark.asyncio
async def test_add_item_sale_not_found(service):
    service.repo.get_sale.return_value = None
    with pytest.raises(NotFoundError):
        await service.add_item(1, "ABC", 1)

@pytest.mark.asyncio
async def test_add_item_sale_closed_conflict(service):
    sale = SimpleNamespace(id=1, status=SaleStatus.PAID)
    service.repo.get_sale.return_value = sale
    
    with pytest.raises(ConflictError):
        await service.add_item(1, "ABC", 1)

@pytest.mark.asyncio
async def test_remove_item_success(service):
    service.repo.remove_line.return_value = True
    result = await service.remove_item(1, "ABC", 1)
    assert result.success is True

@pytest.mark.asyncio
async def test_remove_item_not_found(service):
    service.repo.remove_line.return_value = False
    with pytest.raises(NotFoundError):
        await service.remove_item(1, "ABC", 1)

@pytest.mark.asyncio
async def test_set_discount_success(service):
    service.repo.set_discount.return_value = True
    result = await service.set_discount(1, 0.5)
    assert result.success is True

@pytest.mark.asyncio
async def test_set_discount_invalid_range(service):
    with pytest.raises(ConflictError):
        await service.set_discount(1, 1.5) # > 1
    with pytest.raises(ConflictError):
        await service.set_discount(1, -0.1) # < 0

@pytest.mark.asyncio
async def test_set_discount_sale_not_found(service):
    service.repo.set_discount.return_value = False
    with pytest.raises(NotFoundError):
        await service.set_discount(1, 0.5)

@pytest.mark.asyncio
async def test_close_sale_success(service):
    service.repo.set_status.return_value = True
    result = await service.close_sale(1)
    assert result.success is True
    service.repo.set_status.assert_awaited_once_with(1, SaleStatus.PENDING)

@pytest.mark.asyncio
async def test_close_sale_not_found(service):
    service.repo.set_status.return_value = False
    with pytest.raises(NotFoundError):
        await service.close_sale(999)

# --- Pay Sale Tests ---

@pytest.mark.asyncio
async def test_pay_sale_not_found(service):
    service.repo.get_sale.return_value = None
    with pytest.raises(NotFoundError):
        await service.pay_sale(1, 100.0)

@pytest.mark.asyncio
async def test_pay_sale_invalid_state(service):
    sale = SimpleNamespace(status=SaleStatus.OPEN)
    service.repo.get_sale.return_value = sale
    with pytest.raises(InvalidStateError):
        await service.pay_sale(1, 100.0)

@pytest.mark.asyncio
async def test_pay_sale_insufficient_cash(service):
    # Total = 100.0
    line = SimpleNamespace(quantity=1, price_per_unit=100.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PENDING, lines=[line], discount_rate=0.0)
    service.repo.get_sale.return_value = sale
    
    with pytest.raises(BadRequestError):
        await service.pay_sale(1, 50.0)

@pytest.mark.asyncio
async def test_pay_sale_success(service):
    # Total = 100.0, Cash = 120.0, Change = 20.0
    line = SimpleNamespace(quantity=1, price_per_unit=100.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PENDING, lines=[line], discount_rate=0.0)
    service.repo.get_sale.return_value = sale
    
    with patch("app.services.sale_service.SystemRepository") as MockSys:
        mock_sys_instance = AsyncMock()
        MockSys.return_value = mock_sys_instance
        
        result = await service.pay_sale(1, 120.0)
        
        assert result["change"] == 20.0
        service.repo.set_status.assert_awaited_once_with(1, SaleStatus.PAID)
        mock_sys_instance.update_balance.assert_awaited_once_with(100.0)

# --- Compute Points Tests ---

@pytest.mark.asyncio
async def test_compute_points_not_found(service):
    service.repo.get_sale.return_value = None
    with pytest.raises(NotFoundError):
        await service.compute_points(1)

@pytest.mark.asyncio
async def test_compute_points_invalid_state(service):
    sale = SimpleNamespace(status=SaleStatus.PENDING)
    service.repo.get_sale.return_value = sale
    with pytest.raises(InvalidStateError):
        await service.compute_points(1)

@pytest.mark.asyncio
async def test_compute_points_success(service):
    # Total = 55.0 => Points = 5
    line = SimpleNamespace(quantity=1, price_per_unit=55.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PAID, lines=[line], discount_rate=0.0)
    service.repo.get_sale.return_value = sale
    
    result = await service.compute_points(1)
    assert result["points"] == 5