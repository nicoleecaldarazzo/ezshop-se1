import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.services.customer_service import CustomerService
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.customer_card_error import CustomerCardError

from app.models.DTO.customer_dto import CustomerCreateDTO, LoyaltyCardDTO


@pytest.fixture
def service():
    s = CustomerService()
    s.repo = MagicMock()
    s.repo.create_customer = AsyncMock()
    s.repo.create_card = AsyncMock()
    s.repo.attach_card = AsyncMock()
    s.repo.update_customer = AsyncMock()
    s.repo.delete_customer = AsyncMock()
    s.repo.update_card_points = AsyncMock()

    s._get_customer = AsyncMock()
    s._get_customer_with_card = AsyncMock()
    s._get_card_by_card_id = AsyncMock()
    s._check_customer_has_card = AsyncMock()
    s._check_card_attached = AsyncMock()

    return s


@pytest.mark.asyncio
async def test_create_customer_ok_without_card():
    service = CustomerService()

    service.repo.get_customer_by_name = AsyncMock(return_value=None)
    service.repo.create_customer = AsyncMock(return_value=type("Obj", (), {"id": 1, "name": "Mario Rossi"}))
    service._get_customer_with_card = AsyncMock(return_value=type("Obj", (), {
        "id": 1, "name": "Mario Rossi", "loyalty_card": None
    }))

    dto = CustomerCreateDTO(id=1, name="Mario Rossi")
    res = await service.create_customer(dto)

    assert res.id == 1
    assert res.name == "Mario Rossi"

@pytest.mark.asyncio
async def test_create_customer_invalid_id_raises_bad_request(service):
    service.repo.get_customer_by_name = AsyncMock(side_effect=BadRequestError("Customer ID must be greater than 0"))

    dto = CustomerCreateDTO(id=-1, name="Mario Rossi")

    with pytest.raises(BadRequestError):
        await service.create_customer(dto)

@pytest.mark.asyncio
async def test_create_customer_repo_returns_none_raises(service):
    dto = SimpleNamespace(id=1, name="Alice", card=None)

    service.repo.create_customer.return_value = None

    with pytest.raises(Exception):
        await service.create_customer(dto)

@pytest.mark.asyncio
async def test_create_customer_with_existing_card_raises_conflict(service):
    service.repo.get_customer_by_name = AsyncMock(return_value=None)

    fake_card = SimpleNamespace(card_id="1234567890", points=0, customer_id=99)
    service._get_card_by_card_id = AsyncMock(return_value=fake_card)

    dto = CustomerCreateDTO(
        id=1,
        name="Mario Rossi",
        card=LoyaltyCardDTO(card_id="1234567890", points=0),
    )

    with pytest.raises(ConflictError):
        await service.create_customer(dto)

@pytest.mark.asyncio
async def test_create_customer_with_card_attaches_existing_card(service):
    nested_card = SimpleNamespace(card_id="1234567890", points=10)
    dto = SimpleNamespace(id=1, name="Alice", card=nested_card)

    service.repo.get_customer_by_name = AsyncMock(return_value=None)

    existing_card = SimpleNamespace(card_id="1234567890", points=0, customer_id=None)
    service._get_card_by_card_id = AsyncMock(return_value=existing_card)

    created_customer = SimpleNamespace(id=1, name="Alice", loyalty_card=None)
    service.repo.create_customer = AsyncMock(return_value=created_customer)

    service.repo.attach_card = AsyncMock(return_value=True)

    full_customer = SimpleNamespace(
        id=1,
        name="Alice",
        loyalty_card=SimpleNamespace(card_id="1234567890", points=0),
    )
    service._get_customer_with_card = AsyncMock(return_value=full_customer)

    result = await service.create_customer(dto)

    assert result.id == 1
    assert result.card.card_id == "1234567890"

    service.repo.attach_card.assert_awaited_once_with(1, "1234567890")

@pytest.mark.asyncio
async def test_create_customer_card_creation_fails(service):
    nested = SimpleNamespace(card_id="1234567890", points=10)
    dto = SimpleNamespace(id=1, name="Alice", card=nested)

    service._get_card_by_card_id.return_value = None
    service.repo.create_customer.return_value = SimpleNamespace(id=1, name="Alice")
    service.repo.create_card.return_value = None  

    with pytest.raises(Exception):
        await service.create_customer(dto)

@pytest.mark.asyncio
async def test_get_customer_not_found_raises(service):
    service._get_customer_with_card.side_effect = NotFoundError("not found")

    with pytest.raises(NotFoundError):
        await service.get_customer(999)

@pytest.mark.asyncio
async def test_get_customer_ok(service):
    dao = SimpleNamespace(
        id=1,
        name="Alice",
        loyalty_card=SimpleNamespace(card_id="1234567890", points=5),
    )
    service._get_customer_with_card.return_value = dao

    result = await service.get_customer(1)

    assert result.id == 1
    assert result.name == "Alice"
    assert result.card.card_id == "1234567890"
    assert result.card.points == 5

@pytest.mark.asyncio
async def test__get_customer_ok_uses_repo():
    s = CustomerService()
    s.repo = MagicMock()
    s.repo.get_customer_by_id = AsyncMock(
        return_value=SimpleNamespace(id=1, name="Alice")
    )

    result = await s._get_customer(1)

    s.repo.get_customer_by_id.assert_awaited_once_with(1)
    assert result.id == 1
    assert result.name == "Alice"


@pytest.mark.asyncio
async def test__get_customer_invalid_id_raises_bad_request():
    s = CustomerService()
    with pytest.raises(BadRequestError):
        await s._get_customer(0)


@pytest.mark.asyncio
async def test__get_customer_not_found_raises_not_found():
    s = CustomerService()
    s.repo = MagicMock()
    s.repo.get_customer_by_id = AsyncMock(return_value=None)

    with pytest.raises(NotFoundError):
        await s._get_customer(999)

@pytest.mark.asyncio
async def test_update_customer_invalid_id_raises(service):
    dto = SimpleNamespace(name="New name", card=None)

    with pytest.raises(BadRequestError):
        await service.update_customer(0, dto)

@pytest.mark.asyncio
async def test_update_customer_not_found_raises(service):
    dto = SimpleNamespace(name="New name", card=None)
    service._get_customer.side_effect = NotFoundError("not found")

    with pytest.raises(NotFoundError):
        await service.update_customer(10, dto)

@pytest.mark.asyncio
async def test_update_customer_repo_returns_none_raises(service):
    dto = SimpleNamespace(name="New name", card=None)

    service._get_customer.return_value = SimpleNamespace(id=1)
    service.repo.update_customer.return_value = None

    with pytest.raises(NotFoundError):
        await service.update_customer(1, dto)

@pytest.mark.asyncio
async def test_update_customer_ok(service):
    dto = SimpleNamespace(name="New name", card=None)

    service._get_customer.return_value = SimpleNamespace(id=1)
    service.repo.update_customer.return_value = SimpleNamespace(id=1)
    full = SimpleNamespace(id=1, name="New name", loyalty_card=None)
    service._get_customer_with_card.return_value = full

    result = await service.update_customer(1, dto)

    service.repo.update_customer.assert_awaited_once_with(1, dto)
    assert result.name == "New name"


@pytest.mark.asyncio
async def test_delete_customer_ok(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service.repo.delete_customer.return_value = True

    result = await service.delete_customer(1)

    service.repo.delete_customer.assert_awaited_once_with(1)
    assert result is True

@pytest.mark.asyncio
async def test_delete_customer_non_existing_raises(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service.repo.delete_customer.return_value = False

    with pytest.raises(NotFoundError):
        await service.delete_customer(1)


@pytest.mark.asyncio
async def test_create_customer_card_generation_fails_after_retries(service):
    service._generate_card_id = lambda: "1234567890"
    service.repo.get_card_by_card_id = AsyncMock(return_value=SimpleNamespace(card_id="1234567890"))

    with pytest.raises(Exception):
        await service.create_customer_card()

@pytest.mark.asyncio
async def test_create_card_on_conflict(service):
    service._generate_card_id = lambda: "1234567890"
    service.repo.get_card_by_card_id = AsyncMock(side_effect=[SimpleNamespace(card_id="1234567890"), None])

    created = SimpleNamespace(card_id="1234567890", points=0)
    service.repo.create_card = AsyncMock(return_value=created)

    result = await service.create_customer_card()
    assert result.card_id == "1234567890"

@pytest.mark.asyncio
async def test_create_customer_card_ok(service):
    service.repo.get_card_by_card_id = AsyncMock(return_value=None)

    created = SimpleNamespace(card_id="1234567890", points=0)
    service.repo.create_card = AsyncMock(return_value=created)

    service._generate_card_id = lambda: "1234567890"

    result = await service.create_customer_card()

    assert result.card_id == "1234567890"
    assert result.points == 0
    service.repo.create_card.assert_awaited()

@pytest.mark.asyncio
async def test_get_card_not_found_raises(service):
    service._get_card_by_card_id.return_value = None

    with pytest.raises(NotFoundError):
        await service.get_card("1234567890")

@pytest.mark.asyncio
async def test_create_card_repo_returns_none_raises(service):
    dto = SimpleNamespace(card_id="1234567890", points=5)
    service._get_card_by_card_id.return_value = None
    service.repo.create_card.return_value = None  

    with pytest.raises(Exception):
        await service.create_card(dto)

@pytest.mark.asyncio
async def test_get_card_ok(service):
    card = SimpleNamespace(card_id="1234567890", points=40)
    service._get_card_by_card_id.return_value = card

    result = await service.get_card("1234567890")

    assert result.card_id == "1234567890"
    assert result.points == 40

@pytest.mark.asyncio
async def test_attach_card_empty_card_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.attach_card(1, "")

@pytest.mark.asyncio
async def test_attach_card_card_not_found_raises(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service._check_customer_has_card.return_value = None
    service._get_card_by_card_id.return_value = None

    with pytest.raises(NotFoundError):
        await service.attach_card(1, "1234567890")

@pytest.mark.asyncio
async def test_attach_card_repo_returns_none_raises(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service._check_customer_has_card.return_value = None
    service._get_card_by_card_id.return_value = SimpleNamespace(
        card_id="1234567890", points=5, customer_id=None
    )
    service._check_card_attached.return_value = None
    service.repo.attach_card.return_value = None 

    with pytest.raises(Exception):
        await service.attach_card(1, "1234567890")

@pytest.mark.asyncio
async def test_attach_card_customer_already_has_card_raises(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service._check_customer_has_card.side_effect = ConflictError("already has card")

    with pytest.raises(ConflictError):
        await service.attach_card(1, "1234567890")

@pytest.mark.asyncio
async def test_attach_card_success(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service._check_customer_has_card.return_value = None
    service._get_card_by_card_id.return_value = SimpleNamespace(
        card_id="1234567890", points=5, customer_id=None
    )
    service._check_card_attached.return_value = None

    updated_customer = SimpleNamespace(
        id=1,
        name="Alice",
        loyalty_card=SimpleNamespace(card_id="1234567890", points=5),
    )
    service.repo.attach_card.return_value = updated_customer
    service._get_customer_with_card.return_value = updated_customer

    result = await service.attach_card(1, "1234567890")

    service.repo.attach_card.assert_awaited_once_with(1, "1234567890")
    assert result.id == 1
    assert result.card.card_id == "1234567890"

@pytest.mark.asyncio
async def test__check_customer_has_card_ok():
    s = CustomerService()
    s._get_customer_with_card = AsyncMock(
        return_value=SimpleNamespace(id=1, loyalty_card=None)
    )
    await s._check_customer_has_card(1)

@pytest.mark.asyncio
async def test__check_customer_has_card_raises_conflict():
    s = CustomerService()
    s._get_customer_with_card = AsyncMock(
        return_value=SimpleNamespace(
            id=1,
            loyalty_card=SimpleNamespace(card_id="1234567890", points=10),
        )
    )

    with pytest.raises(ConflictError):
        await s._check_customer_has_card(1)


@pytest.mark.asyncio
async def test__check_card_attached_ok():
    s = CustomerService()
    card = SimpleNamespace(card_id="1234567890", customer_id=None)
    await s._check_card_attached(card)

@pytest.mark.asyncio
async def test__check_card_attached_raises_conflict():
    s = CustomerService()
    card = SimpleNamespace(card_id="1234567890", customer_id=1)
    with pytest.raises(ConflictError):
        await s._check_card_attached(card)

def test__to_customer_response_without_card():
    s = CustomerService()
    customer = SimpleNamespace(id=1, name="Alice", loyalty_card=None)

    result = s._to_customer_response(customer)

    assert result.id == 1
    assert result.name == "Alice"
    assert result.card is None


def test__to_customer_response_with_card():
    s = CustomerService()
    customer = SimpleNamespace(
        id=1,
        name="Alice",
        loyalty_card=SimpleNamespace(card_id="1234567890", points=15),
    )

    result = s._to_customer_response(customer)

    assert result.id == 1
    assert result.card is not None
    assert isinstance(result.card, LoyaltyCardDTO)
    assert result.card.card_id == "1234567890"
    assert result.card.points == 15


@pytest.mark.asyncio
async def test_update_card_points_card_not_found_raises(service):
    service._get_card_by_card_id.return_value = None

    with pytest.raises(NotFoundError):
        await service.update_card_points("1234567890", 7)

    service._get_card_by_card_id.assert_awaited_once_with("1234567890")
    service.repo.update_card_points.assert_not_called()

@pytest.mark.asyncio
async def test_update_card_points_adds_points(service):

    existing_card = SimpleNamespace(card_id="1234567890", points=100)
    service._get_card_by_card_id.return_value = existing_card

    updated_card = SimpleNamespace(card_id="1234567890", points=130)
    service.repo.update_card_points.return_value = updated_card

    result = await service.update_card_points("1234567890", 30)

    service._get_card_by_card_id.assert_awaited_once_with("1234567890")
    service.repo.update_card_points.assert_awaited_once_with("1234567890", 130)

    assert isinstance(result, LoyaltyCardDTO)
    assert result.card_id == "1234567890"
    assert result.points == 130

@pytest.mark.asyncio
async def test_update_card_points_subtracts_points(service):

    existing_card = SimpleNamespace(card_id="1234567890", points=80)
    service._get_card_by_card_id.return_value = existing_card

    updated_card = SimpleNamespace(card_id="1234567890", points=50)
    service.repo.update_card_points.return_value = updated_card

    result = await service.update_card_points("1234567890", -30)

    service._get_card_by_card_id.assert_awaited_once_with("1234567890")
    service.repo.update_card_points.assert_awaited_once_with("1234567890", 50)

    assert result.card_id == "1234567890"
    assert result.points == 50

@pytest.mark.asyncio
async def test_update_card_points_insufficient_points_raises(service):

    existing_card = SimpleNamespace(card_id="1234567890", points=20)
    service._get_card_by_card_id.return_value = existing_card

    with pytest.raises(CustomerCardError):
        await service.update_card_points("1234567890", -50)

    service._get_card_by_card_id.assert_awaited_once_with("1234567890")
    service.repo.update_card_points.assert_not_called()

@pytest.mark.asyncio
async def test_update_card_points_invalid_card_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.update_card_points("", 10)

@pytest.mark.asyncio
async def test_get_card_empty_id_raises(service):
    with pytest.raises(BadRequestError):
        await service.get_card("")

@pytest.mark.asyncio
async def test__get_card_by_card_id_empty_returns_none():
    s = CustomerService()
    result = await s._get_card_by_card_id("")
    assert result is None