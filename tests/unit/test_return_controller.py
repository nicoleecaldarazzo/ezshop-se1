import pytest
from unittest.mock import AsyncMock, MagicMock
from app.controllers.return_controller import ReturnController
from app.models.DTO.return_dto import ReturnDTO
from app.models.return_status import ReturnStatus

@pytest.fixture
def controller():
    """Fixture to create a controller with a mocked service."""
    c = ReturnController()
    c.service = AsyncMock()
    return c

@pytest.mark.asyncio
async def test_create_return_calls_service(controller):
    fake_dto = ReturnDTO(
        id=1, 
        sale_id=10, 
        status=ReturnStatus.OPEN, 
        lines=[], 
        created_at=None, 
        closed_at=None
    )
    controller.service.create_return.return_value = fake_dto

    result = await controller.create_return(sale_id=10)

    controller.service.create_return.assert_awaited_once_with(10)
    assert result.id == 1
    assert result.sale_id == 10

@pytest.mark.asyncio
async def test_reimburse_return_calls_service(controller):
    expected_response = {"refund_amount": 50.0}
    controller.service.reimburse_return.return_value = expected_response

    result = await controller.reimburse_return(return_id=1)

    controller.service.reimburse_return.assert_awaited_once_with(1)
    assert result["refund_amount"] == 50.0

@pytest.mark.asyncio
async def test_close_return_calls_service(controller):
    controller.service.close_return.return_value = True

    result = await controller.close_return(return_id=1)

    # The controller wraps the boolean in a dictionary {"success": True}
    controller.service.close_return.assert_awaited_once_with(1)
    assert result == {"success": True}

@pytest.mark.asyncio
async def test_add_item_calls_service(controller):
    controller.service.add_item.return_value = True

    result = await controller.add_item(return_id=1, barcode="123", amount=2)

    controller.service.add_item.assert_awaited_once_with(1, "123", 2)
    assert result is True
