import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routes.accounting_route import router
from app.models.user_type import UserType
from app.config.config import ROUTES


app = FastAPI()
app.include_router(router)

# Mock Authentication 
async def mock_auth_admin():
    return {"username": "admin", "type": UserType.Administrator}

for route in app.routes:
    if hasattr(route, "dependencies"):
        for dep in route.dependencies:
            app.dependency_overrides[dep.dependency] = mock_auth_admin

client = TestClient(app)
BASE_URL = ROUTES["V1_BALANCE"] 

def test_get_balance_route_200():
    """Test GET /api/v1/balance returns 200 OK and the balance."""
    # Mock the controller's get_balance method
    with patch("app.routes.accounting_route.controller") as mock_controller:
        mock_controller.get_balance = AsyncMock(return_value=500.0)
        
        response = client.get(BASE_URL, headers={"Authorization": "Bearer fake_token"})
        
        assert response.status_code == 200
        assert response.json()["balance"] == 500.0

def test_set_balance_route_201():
    """Test POST /api/v1/balance/set returns 201 Created."""
    # Mock the controller
    with patch("app.routes.accounting_route.controller") as mock_controller:
        mock_controller.set_balance = AsyncMock(return_value=True)
        
        response = client.post(f"{BASE_URL}/set?amount=200", headers={"Authorization": "Bearer fake_token"})
        
        assert response.status_code == 201
        assert response.json()["success"] is True

def test_reset_balance_route_205():
    """Test POST /api/v1/balance/reset returns 205 Reset Content."""
    # Mock the controller
    with patch("app.routes.accounting_route.controller") as mock_controller:
        mock_controller.reset_balance = AsyncMock(return_value=None)
        
        response = client.post(f"{BASE_URL}/reset", headers={"Authorization": "Bearer fake_token"})
        
        assert response.status_code == 205
