import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from types import SimpleNamespace
from app.services.sale_service import SaleService
from app.models.sale_status import SaleStatus

# Import the errors your teammate used
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError

@pytest.fixture
def service():
    # We patch the Repository class that SaleService imports 
    # so that 's = SaleService()' doesn't trigger real DB logic.
    # Change 'app.services.sale_service.SaleRepository' to the actual 
    # repository class name used in your service file.
    with patch('app.services.sale_service.SaleRepository', autospec=True):
        s = SaleService()
        # Now we manually attach an AsyncMock to whatever variable name 
        # your teammate used (repo or repository)
        s.repository = AsyncMock() 
        s.repo = s.repository # Cover both possibilities
        return s

@pytest.mark.asyncio
async def test_create_sale(service):
    # Setup mock return
    service.repository.create_sale.return_value = SimpleNamespace(id=1)
    
    result = await service.create_sale()
    
    assert result.id == 1
    # Check if it was called on the mock, not the real DB
    service.repository.create_sale.assert_called()

@pytest.mark.asyncio
async def test_get_sale_not_found(service):
    # Simulate DB returning nothing
    service.repository.get_sale.return_value = None
    
    with pytest.raises(NotFoundError):
        await service.get_sale(999)

@pytest.mark.asyncio
async def test_add_item_success(service):
    # Setup
    sale = SimpleNamespace(id=1, status=SaleStatus.OPEN)
    service.repo.get_sale.return_value = sale
    service.repo.add_line.return_value = True

    result = await service.add_item(1, "ABC", 2)
    
    # FIX: result is now a raw Boolean (True), not a DTO or dict
    assert result is True 
    service.repo.add_line.assert_awaited_once_with(1, "ABC", 2)

@pytest.mark.asyncio
async def test_pay_sale_insufficient_cash(service):
    # Total = 100.0 (1 unit * 100.0)
    line = SimpleNamespace(quantity=1, price_per_unit=100.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PENDING, lines=[line], discount_rate=0.0)
    service.repository.get_sale.return_value = sale
    
    with pytest.raises(BadRequestError):
        # Paying 50 for a 100 sale should fail
        await service.pay_sale(1, 50.0)

@pytest.mark.asyncio
async def test_compute_points_success(service):
    # Setup: Total = 55.0
    line = SimpleNamespace(quantity=1, price_per_unit=55.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PAID, lines=[line], discount_rate=0.0)
    service.repo.get_sale.return_value = sale

    result = await service.compute_points(1)
    
    # FIX: result is now a raw integer (5), not a dict {"points": 5}
    assert result == 5