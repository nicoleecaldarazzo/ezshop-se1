import pytest
from unittest.mock import AsyncMock, MagicMock
from app.controllers.accounting_controller import AccountingController
from app.models.errors.bad_request import BadRequestError

@pytest.mark.asyncio
async def test_get_balance_success():
    """Test retrieving the balance successfully."""

    controller = AccountingController()
    
    # Mock the repository
    controller.repo.get_balance = AsyncMock(return_value=500.00)

    result = await controller.get_balance()

    assert result == 500.00
    controller.repo.get_balance.assert_called_once()


@pytest.mark.asyncio
async def test_set_balance_success():
    """Test manually setting the balance."""
    controller = AccountingController()
    # Mock the repository to return True (success)
    controller.repo.set_balance = AsyncMock(return_value=True)

    result = await controller.set_balance(100.0)

    assert result is True
    controller.repo.set_balance.assert_called_with(100.0)


@pytest.mark.asyncio
async def test_set_balance_negative_fails():
    """Test that setting a negative balance raises BadRequestError."""
    controller = AccountingController()
    with pytest.raises(BadRequestError):
        await controller.set_balance(-50.0)


@pytest.mark.asyncio
async def test_reset_balance():
    """Test that reset sets the balance to 0.0."""
    controller = AccountingController()
    controller.repo.set_balance = AsyncMock()

    await controller.reset_balance()

    controller.repo.set_balance.assert_called_with(0.0)
