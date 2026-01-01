# tests/integration/test_customer_route.py

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.routes.customer_route import router
from app.models.DTO.customer_dto import CustomerResponseDTO, LoyaltyCardDTO
from app.models.user_type import UserType
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.customer_card_error import CustomerCardError

from app.config.config import ROUTES

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

@app.exception_handler(CustomerCardError)
async def customer_card_handler(request: Request, exc: CustomerCardError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


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

BASE = ROUTES["V1_CUSTOMERS"]

# POST /customers  – Create a new customer

def test_post_customers_201_created_with_card():
    payload = {
        "id": 5,
        "name": "Mario Rossi",
        "card": {
            "card_id": "0000000123",
            "points": 120,
        },
    }

    fake_response = CustomerResponseDTO(
        id=5,
        name="Mario Rossi",
        card=LoyaltyCardDTO(card_id="0000000123", points=120),
    )

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.create_customer = AsyncMock(return_value=fake_response)
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 5
        assert data["name"] == "Mario Rossi"
        assert data["card"]["card_id"] == "0000000123"
        assert data["card"]["points"] == 120


def test_post_customers_400_invalid_input():
    """empty or missing name"""
    payload = {
        "id": 6,
        "name": "",
        "card": None,
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code in (400, 422)


# GET /customers – List all customers

def test_get_customers_200_list_of_customers():
    fake_list = [
        CustomerResponseDTO(
            id=10,
            name="Mario Rossi",
            card=LoyaltyCardDTO(card_id="0000000123", points=120),
        ),
        CustomerResponseDTO(id=11, name="Luca Bianchi", card=None),
    ]

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.list_customers = AsyncMock(return_value=fake_list)

        response = client.get(BASE, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(c["id"] == 10 for c in data)
        assert any(c["id"] == 11 for c in data)


# GET /customers/{customer_id} – Get a customer by ID

def test_get_customer_200_found():
    fake_customer = CustomerResponseDTO(
        id=20,
        name="Mario Rossi",
        card=LoyaltyCardDTO(card_id="0000000999", points=50),
    )

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.get_customer = AsyncMock(return_value=fake_customer)

        response = client.get(f"{BASE}/20", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 20
        assert data["name"] == "Mario Rossi"
        assert data["card"]["card_id"] == "0000000999"


def test_get_customer_400_invalid_id():
    """customer_id <= 0 or fails validation"""
    response = client.get(f"{BASE}/0", headers={"Authorization": "Bearer fake"})
    assert response.status_code in (400, 422)


def test_get_customer_404_not_found():
    """ Customer not found """
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.get_customer = AsyncMock(side_effect=NotFoundError("Customer not found"))

        response = client.get(f"{BASE}/999999", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]


# PUT /customers/{customer_id} – Update existing customer

def test_put_customer_201_updated():

    payload = {
        "name": "Mario Updated",
        "card": {
            "card_id": "0000000123",
            "points": 200,
        },
    }

    fake_updated = CustomerResponseDTO(
        id=30,
        name="Mario Updated",
        card=LoyaltyCardDTO(card_id="0000000123", points=200),
    )

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_customer = AsyncMock(return_value=fake_updated)

        response = client.put(f"{BASE}/30", json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code in (200, 201)
        data = response.json()
        assert data["id"] == 30
        assert data["name"] == "Mario Updated"
        assert data["card"]["points"] == 200


def test_put_customer_400_invalid_input():
    """ Invalid customer input (e.g. empty name) """
    payload = {
        "name": "",
        "card": None,
    }

    response = client.put(f"{BASE}/31", json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code in (400, 422)


def test_put_customer_404_not_found():
    """ Customer or card not found """
    payload = {
        "name": "Someone",
        "card": None,
    }

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_customer = AsyncMock(
            side_effect=NotFoundError("Customer not found")
        )

        response = client.put(f"{BASE}/999998", json=payload,
                              headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]


def test_put_customer_409_conflict():
    """  Conflict (e.g. Card conflict) """
    payload = {
        "name": "Mario",
        "card": {
            "card_id": "0000000123",
            "points": 100,
        },
    }

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_customer = AsyncMock(
            side_effect=ConflictError("Card with id '123' is already attached to a customer")
        )

        response = client.put(f"{BASE}/32", json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "already attached" in response.json()["detail"]


# DELETE /customers/{customer_id}

def test_delete_customer_204_deleted():
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.delete_customer = AsyncMock(return_value=True)

        response = client.delete(f"{BASE}/40", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 204


def test_delete_customer_404_not_found():
    """ Customer not found """
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.delete_customer = AsyncMock(
            side_effect=NotFoundError("Customer not found")
        )

        response = client.delete(f"{BASE}/999997", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]


# POST /customers/cards – Create card

def test_post_customers_cards_201_created():
    payload = {"card_id": "0000000555", "points": 0}

    fake_card = LoyaltyCardDTO(card_id="0000000555", points=0)

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.create_card = AsyncMock(return_value=fake_card)

        response = client.post(f"{BASE}/cards", json=payload,
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["card_id"] == "0000000555"
        assert data["points"] == 0


# PATCH /customers/{customer_id}/attach-card/{card_id}

def test_patch_attach_card_201_attached():

    fake_customer = CustomerResponseDTO(
        id=50,
        name="Mario Attached",
        card=LoyaltyCardDTO(card_id="0000000666", points=100),
    )

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.attach_card = AsyncMock(return_value=fake_customer)

        response = client.patch(f"{BASE}/50/attach-card/0000000666",
                                headers={"Authorization": "Bearer fake"})

        assert response.status_code in (200, 201)
        data = response.json()
        assert data["id"] == 50
        assert data["card"]["card_id"] == "0000000666"


def test_patch_attach_card_400_invalid_ids():
    """ Invalid or empty IDs """
    # invalid card_id that does not match regex ^\\d{10}$
    response = client.patch(f"{BASE}/51/attach-card/abc", headers={"Authorization": "Bearer fake"})
    assert response.status_code in (400, 422)


def test_patch_attach_card_404_not_found():
    """ Customer or card not found """
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.attach_card = AsyncMock(
            side_effect=NotFoundError("Customer or Card not found")
        )

        response = client.patch(f"{BASE}/999996/attach-card/0000000777",
                                headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_patch_attach_card_409_already_attached():
    """ Card already attached to another customer """
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.attach_card = AsyncMock(
            side_effect=ConflictError("Card with id '123' is already attached to a customer")
        )

        response = client.patch(f"{BASE}/52/attach-card/0000000888",
                                headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "already attached" in response.json()["detail"]


# PATCH /customers/cards/{card_id}?points=

def test_patch_cards_add_points_success():
    fake_card = LoyaltyCardDTO(card_id="0000000123", points=150)

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_card_points = AsyncMock(return_value=fake_card)

        response = client.patch(
            f"{BASE}/cards/0000000123",
            params={"points": 30},
            headers={"Authorization": "Bearer fake"},
        )

        assert response.status_code in (200, 201)
        data = response.json()
        assert data["card_id"] == "0000000123"
        assert data["points"] == 150


def test_patch_cards_subtract_points_success():
    fake_card = LoyaltyCardDTO(card_id="0000000123", points=80)

    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_card_points = AsyncMock(return_value=fake_card)

        response = client.patch(
            f"{BASE}/cards/0000000123",
            params={"points": -20},
            headers={"Authorization": "Bearer fake"},
        )

        assert response.status_code in (200, 201)
        assert response.json()["points"] == 80


def test_patch_cards_insufficient_points():
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_card_points = AsyncMock(
            side_effect=CustomerCardError("Insufficient points on the card")
        )

        response = client.patch(
            f"{BASE}/cards/0000000123",
            params={"points": -200},
            headers={"Authorization": "Bearer fake"},
        )

        assert response.status_code in (400, 500)
        assert "Insufficient" in response.json()["detail"]


def test_patch_cards_card_id_404_not_found():
    with patch("app.routes.customer_route.controller") as mock_controller:
        mock_controller.update_card_points = AsyncMock(
            side_effect=NotFoundError("Customer Card not found")
        )

        response = client.patch(
            f"{BASE}/cards/9999999999",
            params={"points": 10},
            headers={"Authorization": "Bearer fake"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()