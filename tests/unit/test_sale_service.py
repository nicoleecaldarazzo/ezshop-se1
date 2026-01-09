import pytest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace

from app.services.sale_service import SaleService
from app.models.sale_status import SaleStatus
from app.models.errors.invalid_state_error import InvalidStateError
from app.models.errors.bad_request import BadRequestError


@pytest.mark.asyncio
async def test_close_sale_sets_pending_ok():
    service = SaleService()
    service.repo = AsyncMock()

    service.repo.set_status = AsyncMock(return_value=True)

    result = await service.close_sale(10)

    service.repo.set_status.assert_awaited_once_with(10, SaleStatus.PENDING)
    assert result.success is True


@pytest.mark.asyncio
async def test_pay_sale_requires_pending():
    service = SaleService()
    service.repo = AsyncMock()

    sale = SimpleNamespace(
        status=SaleStatus.OPEN,
        lines=[],
        discount_rate=0.0,
    )
    service.repo.get_sale = AsyncMock(return_value=sale)

    with pytest.raises(InvalidStateError):
        await service.pay_sale(10, cash_amount=20.0)


@pytest.mark.asyncio
async def test_pay_sale_insufficient_cash_raises():
    service = SaleService()
    service.repo = AsyncMock()

    sale = SimpleNamespace(
        status=SaleStatus.PENDING,
        discount_rate=0.0,
        lines=[
            SimpleNamespace(quantity=2, price_per_unit=25.0, discount_rate=0.0),  # total = 50
        ],
    )
    service.repo.get_sale = AsyncMock(return_value=sale)

    with pytest.raises(BadRequestError):
        await service.pay_sale(10, cash_amount=10.0)


@pytest.mark.asyncio
async def test_pay_sale_returns_change_and_sets_paid():
    service = SaleService()
    service.repo = AsyncMock()

    # subtotal = (2 * 5) * (1 - 0.0) = 10
    # sale discount = 10% => total = 10 * (1 - 0.1) = 9
    sale = SimpleNamespace(
        status=SaleStatus.PENDING,
        discount_rate=0.1,
        lines=[
            SimpleNamespace(quantity=2, price_per_unit=5.0, discount_rate=0.0),
        ],
    )

    service.repo.get_sale = AsyncMock(return_value=sale)
    service.repo.set_status = AsyncMock(return_value=True)

    # pay_sale creates SystemRepository() inside, so patch it in THIS module path:
    with patch("app.services.sale_service.SystemRepository") as SysRepoMock:
        sys_repo_instance = AsyncMock()
        SysRepoMock.return_value = sys_repo_instance

        result = await service.pay_sale(10, cash_amount=21.0)

    service.repo.set_status.assert_awaited_once_with(10, SaleStatus.PAID)
    sys_repo_instance.update_balance.assert_awaited_once_with(9.0)
    assert result["change"] == 12.0
