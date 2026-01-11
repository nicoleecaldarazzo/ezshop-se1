import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.routes.order_route import router
from app.models.DTO.order_dto import OrderResponseDTO
from app.models.user_type import UserType
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.order_status import OrderStatus

from app.config.config import ROUTES
from datetime import datetime, timezone

app = FastAPI()
app.include_router(router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(BadRequestError)
async def bad_request_handler(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def mock_auth_admin():
    return {
        "username": "admin_test",
        "type": "Administrator",
        "role": UserType.Administrator,
    }


for route in app.routes:
    if hasattr(route, "dependencies"):
        for dep in route.dependencies:
            app.dependency_overrides[dep.dependency] = mock_auth_admin

client = TestClient(app)

BASE = ROUTES["V1_ORDERS"]


def test_post_orders_201_created():
    payload = {
        "product_barcode": "123456789012",
        "quantity": 50,
        "price_per_unit": 799.99
    }

    fake_response = OrderResponseDTO(
        id=1,
        product_barcode="123456789012",
        quantity=50,
        price_per_unit=799.99,
        status=OrderStatus.ISSUED,
        issue_date=datetime.now(timezone.utc)
    )

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_order = AsyncMock(return_value=fake_response)
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["product_barcode"] == "123456789012"
        assert data["quantity"] == 50
        assert data["price_per_unit"] == 799.99
        assert data["status"] == OrderStatus.ISSUED


def test_post_orders_400_invalid_barcode():
    payload = {
        "product_barcode": "123",
        "quantity": 10,
        "price_per_unit": 29.99
    }

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_order = AsyncMock(
            side_effect=BadRequestError("Barcode must be a string of 12-14 digits")
        )
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 400
        assert "Barcode" in response.json()["detail"]


def test_post_orders_400_empty_barcode():
    payload = {
        "product_barcode": "",
        "quantity": 10,
        "price_per_unit": 29.99
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_orders_400_negative_quantity():
    payload = {
        "product_barcode": "123456789012",
        "quantity": -5,
        "price_per_unit": 29.99
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_orders_400_zero_quantity():
    payload = {
        "product_barcode": "123456789012",
        "quantity": 0,
        "price_per_unit": 29.99
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_orders_400_negative_price():
    payload = {
        "product_barcode": "123456789012",
        "quantity": 10,
        "price_per_unit": -10.0
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_orders_400_zero_price():
    payload = {
        "product_barcode": "123456789012",
        "quantity": 10,
        "price_per_unit": 0.0
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_orders_404_product_not_found():
    payload = {
        "product_barcode": "999999999999",
        "quantity": 10,
        "price_per_unit": 29.99
    }

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_order = AsyncMock(
            side_effect=NotFoundError("Product not found")
        )
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_get_orders_200_list_of_orders():
    fake_list = [
        OrderResponseDTO(
            id=1,
            product_barcode="123456789012",
            quantity=50,
            price_per_unit=799.99,
            status=OrderStatus.ISSUED,
            issue_date=datetime.now(timezone.utc)
        ),
        OrderResponseDTO(
            id=2,
            product_barcode="987654321098",
            quantity=100,
            price_per_unit=19.99,
            status=OrderStatus.PAID,
            issue_date=datetime.now(timezone.utc)
        )
    ]

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.list_orders = AsyncMock(return_value=fake_list)

        response = client.get(BASE, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert any(o["id"] == 1 for o in data)
        assert any(o["id"] == 2 for o in data)


def test_get_orders_200_empty_list():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.list_orders = AsyncMock(return_value=[])

        response = client.get(BASE, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        assert response.json() == []


def test_post_payfor_201_created():
    payload = {
        "product_barcode": "123456789012",
        "quantity": 30
    }

    fake_response = OrderResponseDTO(
        id=3,
        product_barcode="123456789012",
        quantity=30,
        price_per_unit=799.99,
        status=OrderStatus.PAID,
        issue_date=datetime.now(timezone.utc)
    )

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_and_pay_order = AsyncMock(return_value=fake_response)
        response = client.post(f"{BASE}/payfor", json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 3
        assert data["product_barcode"] == "123456789012"
        assert data["quantity"] == 30
        assert data["status"] == OrderStatus.PAID


def test_post_payfor_400_invalid_barcode():
    payload = {
        "product_barcode": "123",
        "quantity": 10
    }

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_and_pay_order = AsyncMock(
            side_effect=BadRequestError("Barcode must be a string of 12-14 digits")
        )
        response = client.post(f"{BASE}/payfor", json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 400
        assert "Barcode" in response.json()["detail"]


def test_post_payfor_400_negative_quantity():
    payload = {
        "product_barcode": "123456789012",
        "quantity": -10
    }

    response = client.post(f"{BASE}/payfor", json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_payfor_404_product_not_found():
    payload = {
        "product_barcode": "999999999999",
        "quantity": 10
    }

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.create_and_pay_order = AsyncMock(
            side_effect=NotFoundError("Product not found")
        )
        response = client.post(f"{BASE}/payfor", json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_patch_pay_order_200_success():
    fake_updated = OrderResponseDTO(
        id=1,
        product_barcode="123456789012",
        quantity=50,
        price_per_unit=799.99,
        status=OrderStatus.PAID,
        issue_date=datetime.now(timezone.utc)
    )

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.pay_order = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/pay", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["status"] == OrderStatus.PAID


def test_patch_pay_order_422_invalid_id():
    response = client.patch(f"{BASE}/0/pay", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422

    response = client.patch(f"{BASE}/-1/pay", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_patch_pay_order_404_not_found():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.pay_order = AsyncMock(
            side_effect=NotFoundError("Order with id '999999' not found")
        )

        response = client.patch(f"{BASE}/999999/pay", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_patch_pay_order_409_wrong_status():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.pay_order = AsyncMock(
            side_effect=ConflictError("Order must be in ISSUED state to be paid (current: PAID)")
        )

        response = client.patch(f"{BASE}/1/pay", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "ISSUED state" in response.json()["detail"]


def test_patch_pay_order_409_already_completed():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.pay_order = AsyncMock(
            side_effect=ConflictError("Order must be in ISSUED state to be paid (current: COMPLETED)")
        )

        response = client.patch(f"{BASE}/2/pay", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "ISSUED state" in response.json()["detail"]


def test_patch_arrival_200_success():
    fake_updated = OrderResponseDTO(
        id=1,
        product_barcode="123456789012",
        quantity=50,
        price_per_unit=799.99,
        status=OrderStatus.COMPLETED,
        issue_date=datetime.now(timezone.utc)
    )

    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.record_order_arrival = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/arrival", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["status"] == OrderStatus.COMPLETED


def test_patch_arrival_422_invalid_id():
    response = client.patch(f"{BASE}/0/arrival", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_patch_arrival_404_not_found():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.record_order_arrival = AsyncMock(
            side_effect=NotFoundError("Order with id '999999' not found")
        )

        response = client.patch(f"{BASE}/999999/arrival", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_patch_arrival_409_wrong_status():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.record_order_arrival = AsyncMock(
            side_effect=ConflictError("Order must be in PAID state to record arrival (current: ISSUED)")
        )

        response = client.patch(f"{BASE}/1/arrival", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "PAID state" in response.json()["detail"]


def test_patch_arrival_409_already_completed():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.record_order_arrival = AsyncMock(
            side_effect=ConflictError("Order must be in PAID state to record arrival (current: COMPLETED)")
        )

        response = client.patch(f"{BASE}/2/arrival", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "PAID state" in response.json()["detail"]


def test_patch_arrival_404_product_not_found():
    with patch("app.routes.order_route.controller") as mock_controller:
        mock_controller.record_order_arrival = AsyncMock(
            side_effect=NotFoundError("Product not found")
        )

        response = client.patch(f"{BASE}/1/arrival", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]