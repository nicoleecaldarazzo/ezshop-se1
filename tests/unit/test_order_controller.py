import pytest
from unittest.mock import AsyncMock

from app.controllers.order_controller import OrderController


@pytest.fixture
def controller():
    c = OrderController()
    c.service = AsyncMock()
    return c


@pytest.mark.asyncio
async def test_create_order_calls_service(controller):
    payload = object()
    controller.service.create_order.return_value = "ORDER_CREATED"

    result = await controller.create_order(payload)

    controller.service.create_order.assert_awaited_once_with(payload)
    assert result == "ORDER_CREATED"


@pytest.mark.asyncio
async def test_list_orders_calls_service(controller):
    controller.service.list_orders.return_value = ["ORDER1", "ORDER2"]

    result = await controller.list_orders()

    controller.service.list_orders.assert_awaited_once_with()
    assert result == ["ORDER1", "ORDER2"]


@pytest.mark.asyncio
async def test_create_and_pay_order_calls_service(controller):
    payload = object()
    controller.service.create_and_pay_order.return_value = "ORDER_PAID"

    result = await controller.create_and_pay_order(payload)

    controller.service.create_and_pay_order.assert_awaited_once_with(payload)
    assert result == "ORDER_PAID"


@pytest.mark.asyncio
async def test_pay_order_calls_service(controller):
    payment_dto = object()
    controller.service.pay_order.return_value = "ORDER_PAID"

    result = await controller.pay_order(1, payment_dto)

    controller.service.pay_order.assert_awaited_once_with(1, payment_dto)
    assert result == "ORDER_PAID"


@pytest.mark.asyncio
async def test_record_order_arrival_calls_service(controller):
    arrival_dto = object()
    controller.service.record_order_arrival.return_value = "ORDER_COMPLETED"

    result = await controller.record_order_arrival(1, arrival_dto)

    controller.service.record_order_arrival.assert_awaited_once_with(1, arrival_dto)
    assert result == "ORDER_COMPLETED"