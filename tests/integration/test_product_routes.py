import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.routes.product_route import router
from app.models.DTO.product_dto import ProductResponseDTO
from app.models.user_type import UserType
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError

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

BASE = ROUTES["V1_PRODUCTS"]


def test_post_products_201_created():
    payload = {
        "description": "Laptop HP",
        "barcode": "123456789012",
        "price_per_unit": 799.99,
        "note": "High performance laptop",
        "quantity": 50,
        "position": "1-A-2"
    }

    fake_response = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note="High performance laptop",
        quantity=50,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.create_product = AsyncMock(return_value=fake_response)
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["description"] == "Laptop HP"
        assert data["barcode"] == "123456789012"
        assert data["price_per_unit"] == 799.99
        assert data["quantity"] == 50


def test_post_products_201_created_without_optional_fields():
    payload = {
        "description": "Mouse",
        "barcode": "987654321098",
        "price_per_unit": 19.99,
        "quantity": 100
    }

    fake_response = ProductResponseDTO(
        id=2,
        description="Mouse",
        barcode="987654321098",
        price_per_unit=19.99,
        note=None,
        quantity=100,
        position=None
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.create_product = AsyncMock(return_value=fake_response)
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["note"] is None
        assert data["position"] is None


def test_post_products_400_invalid_barcode():
    payload = {
        "description": "Test Product",
        "barcode": "123",
        "price_per_unit": 29.99,
        "quantity": 10
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_products_400_negative_price():
    payload = {
        "description": "Test Product",
        "barcode": "123456789012",
        "price_per_unit": -10.0,
        "quantity": 10
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_products_400_negative_quantity():
    payload = {
        "description": "Test Product",
        "barcode": "123456789012",
        "price_per_unit": 29.99,
        "quantity": -5
    }

    response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_post_products_409_duplicate_barcode():
    payload = {
        "description": "Duplicate Product",
        "barcode": "123456789012",
        "price_per_unit": 29.99,
        "quantity": 10
    }

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.create_product = AsyncMock(
            side_effect=ConflictError("Product barcode already exists")
        )
        response = client.post(BASE, json=payload, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


def test_get_products_200_list_of_products():
    fake_list = [
        ProductResponseDTO(
            id=1,
            description="Laptop HP",
            barcode="123456789012",
            price_per_unit=799.99,
            note=None,
            quantity=50,
            position="1-A-2"
        ),
        ProductResponseDTO(
            id=2,
            description="Mouse",
            barcode="987654321098",
            price_per_unit=19.99,
            note=None,
            quantity=100,
            position=None
        )
    ]

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.list_products = AsyncMock(return_value=fake_list)

        response = client.get(BASE, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert any(p["id"] == 1 for p in data)
        assert any(p["id"] == 2 for p in data)


def test_get_products_200_empty_list():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.list_products = AsyncMock(return_value=[])

        response = client.get(BASE, headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        assert response.json() == []


def test_get_products_search_200_found():
    fake_results = [
        ProductResponseDTO(
            id=1,
            description="Laptop HP Pavilion",
            barcode="123456789012",
            price_per_unit=799.99,
            note=None,
            quantity=50,
            position="1-A-2"
        ),
        ProductResponseDTO(
            id=3,
            description="Laptop Dell",
            barcode="111122223333",
            price_per_unit=899.99,
            note=None,
            quantity=30,
            position="1-A-3"
        )
    ]

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.search_products = AsyncMock(return_value=fake_results)

        response = client.get(f"{BASE}/search?query=Laptop", 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("Laptop" in p["description"] for p in data)


def test_get_products_search_200_no_results():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.search_products = AsyncMock(return_value=[])

        response = client.get(f"{BASE}/search?query=NonExistent", 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        assert response.json() == []


def test_get_products_search_422_missing_description():
    response = client.get(f"{BASE}/search", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_get_products_search_400_empty_description():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.search_products = AsyncMock(
            side_effect=BadRequestError("Search description cannot be empty")
        )

        response = client.get(f"{BASE}/search?description=", 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code in (400, 422)


def test_get_product_by_barcode_200_found():
    fake_product = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=50,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.get_product_by_barcode = AsyncMock(return_value=fake_product)

        response = client.get(f"{BASE}/barcode/123456789012", 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert data["barcode"] == "123456789012"
        assert data["id"] == 1


def test_get_product_by_barcode_422_invalid_format():
    response = client.get(f"{BASE}/barcode/123", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_get_product_by_barcode_404_not_found():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.get_product_by_barcode = AsyncMock(
            side_effect=NotFoundError("Product with barcode '999999999999' not found")
        )

        response = client.get(f"{BASE}/barcode/999999999999", 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_get_product_200_found():
    fake_product = ProductResponseDTO(
        id=5,
        description="Keyboard",
        barcode="555566667777",
        price_per_unit=49.99,
        note="Mechanical keyboard",
        quantity=75,
        position="2-B-1"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.get_product = AsyncMock(return_value=fake_product)

        response = client.get(f"{BASE}/5", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 5
        assert data["description"] == "Keyboard"


def test_get_product_422_invalid_id():
    response = client.get(f"{BASE}/0", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_get_product_404_not_found():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.get_product = AsyncMock(
            side_effect=NotFoundError("Product with id '999999' not found")
        )

        response = client.get(f"{BASE}/999999", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "Product with id" in response.json()["detail"]


def test_put_product_201_updated():
    payload = {
        "description": "Updated Laptop HP",
        "price_per_unit": 849.99,
        "quantity": 60
    }

    fake_updated = ProductResponseDTO(
        id=1,
        description="Updated Laptop HP",
        barcode="123456789012",
        price_per_unit=849.99,
        note=None,
        quantity=60,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product = AsyncMock(return_value=fake_updated)

        response = client.put(f"{BASE}/1", json=payload, 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Updated Laptop HP"
        assert data["price_per_unit"] == 849.99
        assert data["quantity"] == 60


def test_put_product_201_partial_update():
    payload = {
        "price_per_unit": 899.99
    }

    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=899.99,
        note=None,
        quantity=50,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product = AsyncMock(return_value=fake_updated)

        response = client.put(f"{BASE}/1", json=payload, 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["price_per_unit"] == 899.99


def test_put_product_422_invalid_input():
    payload = {
        "price_per_unit": -100.0
    }

    response = client.put(f"{BASE}/1", json=payload, 
                         headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_put_product_404_not_found():
    payload = {
        "description": "Updated Product"
    }

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product = AsyncMock(
            side_effect=NotFoundError("Product with id '999999' not found")
        )

        response = client.put(f"{BASE}/999999", json=payload, 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_put_product_409_barcode_conflict():
    payload = {
        "barcode": "123456789012"
    }

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product = AsyncMock(
            side_effect=ConflictError("Barcode already exists")
        )

        response = client.put(f"{BASE}/2", json=payload, 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


def test_put_product_409_barcode_has_active_sales():
    payload = {
        "barcode": "999988887777"
    }

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product = AsyncMock(
            side_effect=ConflictError("Product barcode cannot be updated because it has sales associated with it")
        )

        response = client.put(f"{BASE}/1", json=payload, 
                            headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "cannot be updated" in response.json()["detail"]


def test_delete_product_204_deleted():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.delete_product = AsyncMock(return_value=True)

        response = client.delete(f"{BASE}/10", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 204


def test_delete_product_422_invalid_id():
    response = client.delete(f"{BASE}/0", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_delete_product_404_not_found():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.delete_product = AsyncMock(
            side_effect=NotFoundError("Product with id '999999' not found")
        )

        response = client.delete(f"{BASE}/999999", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


def test_delete_product_409_has_active_sales():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.delete_product = AsyncMock(
            side_effect=ConflictError("Product cannot be deleted because it has active sales (OPEN, PENDING, or PAID)")
        )

        response = client.delete(f"{BASE}/1", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "cannot be deleted" in response.json()["detail"]


def test_delete_product_409_has_active_orders():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.delete_product = AsyncMock(
            side_effect=ConflictError("Product cannot be deleted because it has active orders (ISSUED, PAID, or COMPLETED)")
        )

        response = client.delete(f"{BASE}/2", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 409
        assert "active orders" in response.json()["detail"]


def test_patch_product_position_201_updated():
    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=50,
        position="3-C-5"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_position = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/position?position=3-C-5", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["position"] == "3-C-5"


def test_patch_product_position_201_clear_position():
    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=50,
        position=None
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_position = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/position?position=", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201


def test_patch_product_position_422_missing_query():
    response = client.patch(f"{BASE}/1/position", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_patch_product_position_400_invalid_format():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_position = AsyncMock(
            side_effect=BadRequestError("Position must match pattern 'aisle-shelf-level' (e.g., '1-A-2')")
        )

        response = client.patch(f"{BASE}/1/position?position=invalid", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 400
        assert "pattern" in response.json()["detail"]


def test_patch_product_position_404_not_found():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_position = AsyncMock(
            side_effect=NotFoundError("Product with id '999999' not found")
        )

        response = client.patch(f"{BASE}/999999/position?position=1-A-1", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404


def test_patch_product_quantity_201_add_quantity():
    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=150,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_quantity = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/quantity?quantity=100", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 150


def test_patch_product_quantity_201_subtract_quantity():
    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=30,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_quantity = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/quantity?quantity=-20", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 30


def test_patch_product_quantity_201_set_to_zero():
    fake_updated = ProductResponseDTO(
        id=1,
        description="Laptop HP",
        barcode="123456789012",
        price_per_unit=799.99,
        note=None,
        quantity=0,
        position="1-A-2"
    )

    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_quantity = AsyncMock(return_value=fake_updated)

        response = client.patch(f"{BASE}/1/quantity?quantity=-50", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 0


def test_patch_product_quantity_422_missing_query():
    response = client.patch(f"{BASE}/1/quantity", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 422


def test_patch_product_quantity_400_negative_result():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_quantity = AsyncMock(
            side_effect=BadRequestError("Quantity cannot be negative")
        )

        response = client.patch(f"{BASE}/1/quantity?quantity=-1000", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 400
        assert "cannot be negative" in response.json()["detail"]


def test_patch_product_quantity_404_not_found():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.update_product_quantity = AsyncMock(
            side_effect=NotFoundError("Product with id '999999' not found")
        )

        response = client.patch(f"{BASE}/999999/quantity?quantity=10", 
                               headers={"Authorization": "Bearer fake"})

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_get_products_reorder_200_empty_list():
    with patch("app.routes.product_route.controller") as mock_controller:
        mock_controller.get_products_needing_reorder = AsyncMock(return_value=[])

        response = client.get(f"{BASE}/reorder", headers={"Authorization": "Bearer fake"})

        assert response.status_code == 200
        assert response.json() == []
        mock_controller.get_products_needing_reorder.assert_awaited_once()