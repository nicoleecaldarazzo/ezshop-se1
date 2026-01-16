import pytest
from unittest.mock import AsyncMock

from app.controllers.customer_controller import CustomerController


@pytest.fixture
def controller():
    c = CustomerController()
    c.service = AsyncMock()
    return c


# customers CRUD functions

@pytest.mark.asyncio
async def test_create_customer_calls_service(controller):
    payload = object()
    controller.service.create_customer.return_value = "CREATED"

    result = await controller.create_customer(payload)

    controller.service.create_customer.assert_awaited_once_with(payload)
    assert result == "CREATED"


@pytest.mark.asyncio
async def test_get_customer_calls_service(controller):
    controller.service.get_customer.return_value = "CUSTOMER"

    result = await controller.get_customer(1)

    controller.service.get_customer.assert_awaited_once_with(1)
    assert result == "CUSTOMER"


@pytest.mark.asyncio
async def test_list_customers_calls_service(controller):
    controller.service.list_customers.return_value = ["C1", "C2"]

    result = await controller.list_customers()

    controller.service.list_customers.assert_awaited_once_with()
    assert result == ["C1", "C2"]


@pytest.mark.asyncio
async def test_update_customer_calls_service(controller):
    payload = object()
    controller.service.update_customer.return_value = "UPDATED"

    result = await controller.update_customer(1, payload)

    controller.service.update_customer.assert_awaited_once_with(1, payload)
    assert result == "UPDATED"


@pytest.mark.asyncio
async def test_delete_customer_calls_service(controller):
    controller.service.delete_customer.return_value = True

    result = await controller.delete_customer(1)

    controller.service.delete_customer.assert_awaited_once_with(1)
    assert result is True


# loyalty card endpoints

@pytest.mark.asyncio
async def test_create_card_calls_service():
    controller = CustomerController()
    controller.service.create_card = AsyncMock(return_value={"card_id": "1234567890", "points": 0})

    resp = await controller.create_card()

    controller.service.create_card.assert_awaited_once()
    assert resp["card_id"] == "1234567890"
    assert resp["points"] == 0

@pytest.mark.asyncio
async def test_attach_card_calls_service(controller):
    controller.service.attach_card.return_value = "WITH_CARD"

    result = await controller.attach_card(1, "1234567890")

    controller.service.attach_card.assert_awaited_once_with(1, "1234567890")
    assert result == "WITH_CARD"


@pytest.mark.asyncio
async def test_update_card_points_calls_service(controller):
    controller.service.update_card_points.return_value = "UPDATED_CARD"

    result = await controller.update_card_points("1234567890", 10)

    controller.service.update_card_points.assert_awaited_once_with("1234567890", 10)
    assert result == "UPDATED_CARD"


@pytest.mark.asyncio
async def test_get_card_calls_service(controller):
    controller.service.get_card.return_value = "CARD_INFO"

    result = await controller.get_card("1234567890")

    controller.service.get_card.assert_awaited_once_with("1234567890")
    assert result == "CARD_INFO"