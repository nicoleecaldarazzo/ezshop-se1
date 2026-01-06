import pytest
from unittest.mock import AsyncMock

from app.services.sale_service import SaleService
from app.models.sale_status import SaleStatus
from app.models.errors.invalid_state_error import InvalidStateError


@pytest.mark.asyncio
async def test_close_sale_sets_pending():
    repo = AsyncMock()
    service = SaleService(repo)

    sale = AsyncMock()
    sale.status = SaleStatus.OPEN

    repo.get_sale = AsyncMock(return_value=sale)
    repo.update_sale_status = AsyncMock()

    await service.close_sale(10)

    repo.update_sale_status.assert_awaited_once_with(10, SaleStatus.PENDING)


@pytest.mark.asyncio
async def test_pay_sale_requires_pending():
    repo = AsyncMock()
    service = SaleService(repo)

    sale = AsyncMock()
    sale.status = SaleStatus.OPEN  # not pending

    repo.get_sale = AsyncMock(return_value=sale)

    with pytest.raises(InvalidStateError):
        await service.pay_sale(10, cash_amount=10.0)


@pytest.mark.asyncio
async def test_pay_sale_returns_change():
    repo = AsyncMock()
    service = SaleService(repo)

    sale = AsyncMock()
    sale.status = SaleStatus.PENDING
    sale.total = 8.0  # adjust to your attribute name if needed

    repo.get_sale = AsyncMock(return_value=sale)
    repo.update_sale_status = AsyncMock()
    repo.update_balance = AsyncMock()

    res = await service.pay_sale(10, cash_amount=10.0)

    assert "change" in res
    assert res["change"] == 2.0
    repo.update_sale_status.assert_awaited_once()
    repo.update_balance.assert_awaited_once()
