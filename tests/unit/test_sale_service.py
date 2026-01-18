import pytest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace
from app.services.sale_service import SaleService
from app.models.sale_status import SaleStatus
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError

@pytest.fixture
def service():
    # We patch the Repository classes to prevent real DB interaction
    with patch('app.services.sale_service.SaleRepository', autospec=True), \
         patch('app.services.sale_service.ProductRepository', autospec=True):
        s = SaleService()
        s.repo = AsyncMock()
        s.prod_repo = AsyncMock()
        return s

@pytest.mark.asyncio
async def test_add_item_success(service):
    # 1. Setup mocks
    test_barcode = "123456789"
    mock_product = SimpleNamespace(barcode=test_barcode, quantity=100, price_per_unit=10.0)
    mock_sale = SimpleNamespace(id=1, status=SaleStatus.OPEN, lines=[])

    service.repo.get_sale.return_value = mock_sale
    service.prod_repo.get_product_by_barcode.return_value = mock_product
    service.repo.add_line.return_value = True

    # 2. Execute
    result = await service.add_item(sale_id=1, barcode=test_barcode, amount=5)
    
    # 3. Assert
    assert result is True
    service.repo.add_line.assert_called_with(1, test_barcode, 5)

@pytest.mark.asyncio
async def test_get_sale_not_found(service):
    service.repo.get_sale.return_value = None
    with pytest.raises(NotFoundError):
        await service.get_sale(999)

@pytest.mark.asyncio
async def test_pay_sale_insufficient_cash(service):
    line = SimpleNamespace(quantity=1, price_per_unit=100.0, discount_rate=0.0)
    sale = SimpleNamespace(status=SaleStatus.PENDING, lines=[line], discount_rate=0.0)
    service.repo.get_sale.return_value = sale
    
    with pytest.raises(BadRequestError):
        await service.pay_sale(1, 50.0)