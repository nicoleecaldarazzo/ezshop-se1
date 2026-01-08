import pytest
from unittest.mock import patch, AsyncMock
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from app.routes.user_route import router
from app.models.DTO.user_dto import UserResponseDTO
from app.models.user_type import UserType
from app.models.errors.notfound_error import NotFoundError 
from app.models.errors.bad_request import BadRequestError


app = FastAPI()
app.include_router(router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(BadRequestError)
async def bad_request_handler(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def mock_auth_admin():
    return {
        "username": "admin_test",
        "type": "Administrator",
        "role": UserType.Administrator 
    }


for route in app.routes:
    if hasattr(route, "dependencies"):
        for dep in route.dependencies:
            app.dependency_overrides[dep.dependency] = mock_auth_admin

client = TestClient(app)


def test_create_user_route_success():
    """
    Test that the POST /api/v1/users/ route calls the controller and returns 201
    """
    payload = {
        "username": "new_user",
        "password": "secret_password",
        "type": "Cashier"
    }

    fake_response = UserResponseDTO(
        id=1,
        username="new_user",
        type="Cashier"
    )

    with patch("app.routes.user_route.controller") as mock_controller:
        mock_controller.create_user = AsyncMock(return_value=fake_response)

        response = client.post("/api/v1/users/", json=payload, headers={"Authorization": "Bearer fake"})

        if response.status_code != 201:
            print(f"\nERRORE API: {response.json()}")

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "new_user"
        assert data["type"] == "Cashier"

def test_create_user_missing_password():
    """
    Test error if fields are missing
    """
    payload = {
        "username": "no_pass_user",
        "type": "Cashier"
    }

    response = client.post("/api/v1/users/", json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code in [400, 422]

def test_get_user_not_found():
    """
    Test GET /api/v1/users/{id} when the user does not exist
    """
    with patch("app.routes.user_route.controller") as mock_controller:
        mock_controller.get_user = AsyncMock(return_value=None)

        response = client.get("/api/v1/users/999", headers={"Authorization": "Bearer fake"})

        
        assert response.status_code == 404
        
        assert "User not found" in response.json()["detail"]

def test_create_user_empty_password():
    """
    Test manual check for empty password inside the route.
    Questo test colpisce l'if user.password == ''
    """
    payload = {
        "username": "user_empty_pass",
        "password": "", 
        "type": "Cashier"
    }
    
    response = client.post("/api/v1/users/", json=payload, headers={"Authorization": "Bearer fake"})
    
    assert response.status_code == 400
    assert "Password is a mandatory field" in response.json()["detail"]

def test_create_user_empty_type():
    """
    Test manual check for empty type inside the route.
    Questo test colpisce l'if user.type == ''
    """
    payload = {
        "username": "user_empty_type",
        "password": "valid_password",
        "type": ""  
    }
    
    response = client.post("/api/v1/users/", json=payload, headers={"Authorization": "Bearer fake"})
    
    assert response.status_code == 400
    assert "User type is a mandatory field" in response.json()["detail"]