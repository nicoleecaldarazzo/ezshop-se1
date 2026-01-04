import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.routes.return_route import router
from app.models.DTO.return_dto import ReturnDTO
from app.models.user_type import UserType
from app.models.return_status import ReturnStatus
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.conflict_error import ConflictError

app = FastAPI()
app.include_router(router)

# Custom Exception Handlers
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

# Mock Authentication
async def mock_auth_admin():
    return {"username": "admin", "type": UserType.Administrator}

for route in app.routes:
    if hasattr(route, "dependencies"):
        for dep in route.dependencies:
            app.dependency_overrides[dep.dependency] = mock_auth_admin

client = TestClient(app)
BASE_URL = "/api/v1/returns"

def test_create_return_201():
    """Test creating a new return transaction."""
    fake_dto = ReturnDTO(
        id=1, 
        sale_id=10, 
        status=ReturnStatus.OPEN, 
        lines=[], 
        created_at=None, 
        closed_at=None
    )
    
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.create_return = AsyncMock(return_value=fake_dto)
        response = client.post(f"{BASE_URL}/", params={"sale_id": 10}, headers={"Authorization": "Bearer fake"})
        
        assert response.status_code == 201
        assert response.json()["id"] == 1

def test_add_item_201():
    """Test adding an item to the return."""
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.add_item = AsyncMock(return_value=True)
        payload = {"barcode": "123456789012", "amount": 1}
        
        response = client.post(f"{BASE_URL}/1/items", params=payload, headers={"Authorization": "Bearer fake"})
     
        assert response.status_code == 201
        assert response.json()["success"] is True

def test_reimburse_return_200():
    """Test processing the refund."""
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.reimburse_return = AsyncMock(return_value={"refund_amount": 50.0})
        response = client.patch(f"{BASE_URL}/1/reimburse", headers={"Authorization": "Bearer fake"})
        
        assert response.status_code == 200
        assert response.json()["refund_amount"] == 50.0

def test_get_return_404_not_found():
    """Test error handling when return does not exist."""
    with patch("app.routes.return_route.controller") as mock_controller:
        mock_controller.get_return = AsyncMock(side_effect=NotFoundError("Return not found"))
        
        response = client.get(f"{BASE_URL}/999", headers={"Authorization": "Bearer fake"})
        
        assert response.status_code == 404