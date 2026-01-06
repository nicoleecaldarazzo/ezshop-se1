from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routes import return_route  
from app.config.config import ROUTES
from app.models.user_type import UserType


app = FastAPI()
app.include_router(return_route.router)


async def fake_user():
    return {"username": "test_user", "role": UserType.Cashier}


app.dependency_overrides[return_route.auth_dep.dependency] = fake_user

client = TestClient(app)

BASE = ROUTES["V1_RETURNS"] 


def test_start_return_ok():
    fake_return = {"id": 12, "sale_id": 10, "status": "OPEN"}
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.create_return = AsyncMock(return_value=fake_return)
        res = client.post(f"{BASE}/", params={"sale_id": 10})
        assert res.status_code in (200, 201)
        assert res.json()["sale_id"] == 10


def test_get_return_ok():
    fake_return = {"id": 12, "sale_id": 10, "status": "OPEN"}
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.get_return = AsyncMock(return_value=fake_return)
        res = client.get(f"{BASE}/12")
        assert res.status_code == 200
        assert res.json()["id"] == 12
