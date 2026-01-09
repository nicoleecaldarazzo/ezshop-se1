from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers import sale_controller  
from app.models.user_type import UserType


app = FastAPI()
app.include_router(sale_controller.router)


async def fake_user():
    return {"username": "test_cashier", "role": UserType.Cashier}

app.dependency_overrides[sale_controller.auth_dep.dependency] = fake_user

client = TestClient(app)


def test_create_sale_ok():
    fake_sale = {"id": 1, "status": "OPEN"}

    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.create_sale = AsyncMock(return_value=fake_sale)

        res = client.post("/api/v1/sales")
        assert res.status_code == 200
        assert res.json()["status"] == "OPEN"


def test_get_sale_ok():
    fake_sale = {"id": 1, "status": "OPEN"}

    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.get_sale = AsyncMock(return_value=fake_sale)

        res = client.get("/api/v1/sales/1")
        assert res.status_code == 200
        assert res.json()["id"] == 1


def test_add_item_ok():
    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.add_item = AsyncMock(return_value={"ok": True})

        res = client.post(
            "/api/v1/sales/1/items",
            params={"barcode": "1234567890123", "amount": 1},
        )
        assert res.status_code == 200


def test_remove_item_ok():
    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.remove_item = AsyncMock(return_value={"ok": True})

        res = client.delete(
            "/api/v1/sales/1/items",
            params={"barcode": "1234567890123", "amount": 1},
        )
        assert res.status_code == 200


def test_set_discount_ok():
    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.set_discount = AsyncMock(return_value={"ok": True})

        res = client.patch(
            "/api/v1/sales/1/discount",
            params={"discount": 0.1},
        )
        assert res.status_code == 200


def test_close_sale_ok():
    fake_sale = {"id": 1, "status": "PENDING"}

    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.close_sale = AsyncMock(return_value=fake_sale)

        res = client.patch("/api/v1/sales/1/close")
        assert res.status_code == 200
        assert res.json()["status"] == "PENDING"


def test_pay_sale_ok():
    fake_payment = {"change": 21.0}

    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.pay_sale = AsyncMock(return_value=fake_payment)

        res = client.patch(
            "/api/v1/sales/1/pay",
            params={"cash_amount": 50.0},
        )
        assert res.status_code == 200
        assert "change" in res.json()


def test_compute_points_ok():
    with patch("app.controllers.sale_controller.service") as mock_service:
        mock_service.compute_points = AsyncMock(return_value={"points": 10})

        res = client.get("/api/v1/sales/1/points")
        assert res.status_code == 200
