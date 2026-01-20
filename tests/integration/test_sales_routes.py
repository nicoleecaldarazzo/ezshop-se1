import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.models.sale_status import SaleStatus
import app.controllers.sale_controller as sale_controller

@pytest.fixture
def mock_service():
    mock = MagicMock()
    
    # The 'Perfect' dictionary that matches your SaleDTO exactly.
    # We set datetime to None to satisfy the 'none_required' validation error.
    valid_sale_dict = {
        "id": 1,
        "lines": [],
        "status": SaleStatus.OPEN, 
        "datetime": None  # Changed from timestamp to None to fix the error
    }
    
    mock.create_sale = AsyncMock(return_value=valid_sale_dict)
    mock.get_sale = AsyncMock(return_value=valid_sale_dict)
    mock.list_sales = AsyncMock(return_value=[valid_sale_dict])
    
    # Return raw types as expected by our updated service
    mock.add_item = AsyncMock(return_value=True)
    mock.remove_item = AsyncMock(return_value=True)
    mock.close_sale = AsyncMock(return_value=True)
    mock.delete_sale = AsyncMock(return_value=True)
    mock.pay_sale = AsyncMock(return_value=5.0)
    mock.compute_points = AsyncMock(return_value=10)
    
    return mock

@pytest.fixture
def client(mock_service):
    app = FastAPI()
    app.include_router(sale_controller.router)

    # Mock User Auth
    async def fake_user():
        return {"username": "test", "role": "Cashier"}
    
    from app.controllers.sale_controller import auth_dep
    app.dependency_overrides[auth_dep.dependency] = fake_user
    app.dependency_overrides[sale_controller.get_controller] = lambda: mock_service

    return TestClient(app)

# --- TESTS ---

def test_create_sale_endpoint(client):
    res = client.post("/api/v1/sales/")
    assert res.status_code == 201
    assert res.json()["id"] == 1

def test_add_item_endpoint(client):
    res = client.post("/api/v1/sales/1/items", params={"barcode": "123", "amount": 1})
    assert res.status_code == 201

def test_remove_item_endpoint(client):
    res = client.delete("/api/v1/sales/1/items", params={"barcode": "123", "amount": 1})
    assert res.status_code == 202

def test_pay_sale_endpoint(client):
    res = client.patch("/api/v1/sales/1/pay", params={"cash_amount": 50.0})
    assert res.status_code == 200
    assert "change" in res.json()

def test_get_points_endpoint(client):
    res = client.get("/api/v1/sales/1/points")
    assert res.status_code == 200
    assert res.json()["points"] == 10

def test_delete_sale_endpoint(client):
    res = client.delete("/api/v1/sales/1")
    assert res.status_code == 204