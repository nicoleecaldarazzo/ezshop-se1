import pytest
from unittest.mock import AsyncMock

from app.controllers.product_controller import ProductController


@pytest.fixture
def controller():
    c = ProductController()
    c.service = AsyncMock()
    return c


@pytest.mark.asyncio
async def test_create_product_calls_service(controller):
    payload = object()
    controller.service.create_product.return_value = "CREATED"

    result = await controller.create_product(payload)

    controller.service.create_product.assert_awaited_once_with(payload)
    assert result == "CREATED"


@pytest.mark.asyncio
async def test_get_product_calls_service(controller):
    controller.service.get_product.return_value = "PRODUCT"

    result = await controller.get_product(1)

    controller.service.get_product.assert_awaited_once_with(1)
    assert result == "PRODUCT"


@pytest.mark.asyncio
async def test_list_products_calls_service(controller):
    controller.service.list_products.return_value = ["P1", "P2"]

    result = await controller.list_products()

    controller.service.list_products.assert_awaited_once_with()
    assert result == ["P1", "P2"]


@pytest.mark.asyncio
async def test_update_product_calls_service(controller):
    payload = object()
    controller.service.update_product.return_value = "UPDATED"

    result = await controller.update_product(1, payload)

    controller.service.update_product.assert_awaited_once_with(1, payload)
    assert result == "UPDATED"


@pytest.mark.asyncio
async def test_delete_product_calls_service(controller):
    controller.service.delete_product.return_value = True

    result = await controller.delete_product(1)

    controller.service.delete_product.assert_awaited_once_with(1)
    assert result is True


@pytest.mark.asyncio
async def test_get_product_by_barcode_calls_service(controller):
    controller.service.get_product_by_barcode.return_value = "PRODUCT_BY_BARCODE"

    result = await controller.get_product_by_barcode("123456789012")

    controller.service.get_product_by_barcode.assert_awaited_once_with("123456789012")
    assert result == "PRODUCT_BY_BARCODE"


@pytest.mark.asyncio
async def test_search_products_calls_service(controller):
    payload = object()
    controller.service.search_products.return_value = ["P1", "P2", "P3"]

    result = await controller.search_products(payload)

    controller.service.search_products.assert_awaited_once_with(payload)
    assert result == ["P1", "P2", "P3"]


@pytest.mark.asyncio
async def test_update_product_position_calls_service(controller):
    payload = object()
    controller.service.update_product_position.return_value = "UPDATED_POSITION"

    result = await controller.update_product_position(1, payload)

    controller.service.update_product_position.assert_awaited_once_with(1, payload)
    assert result == "UPDATED_POSITION"


@pytest.mark.asyncio
async def test_update_product_quantity_calls_service(controller):
    controller.service.update_product_quantity.return_value = "UPDATED_QUANTITY"

    result = await controller.update_product_quantity(1, 10)

    controller.service.update_product_quantity.assert_awaited_once_with(1, 10)
    assert result == "UPDATED_QUANTITY"

@pytest.mark.asyncio
async def test_get_products_needing_reorder_calls_service(controller):
    controller.service.get_products_needing_reorder.return_value = ["P1", "P2"]

    result = await controller.get_products_needing_reorder()

    controller.service.get_products_needing_reorder.assert_awaited_once_with()
    assert result == ["P1", "P2"]