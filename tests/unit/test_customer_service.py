import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.services.customer_service import CustomerService
from app.models.errors.bad_request import BadRequestError
from app.models.errors.conflict_error import ConflictError
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.customer_card_error import CustomerCardError

from app.models.DTO.customer_dto import LoyaltyCardDTO


@pytest.fixture
def service():
    s = CustomerService()

    # mock repository methods (async)
    s.repo = MagicMock()
    s.repo.create_customer = AsyncMock()
    s.repo.create_card = AsyncMock()
    s.repo.attach_card = AsyncMock()
    s.repo.update_customer = AsyncMock()
    s.repo.delete_customer = AsyncMock()
    s.repo.update_card_points = AsyncMock()

    # mock internal async helpers that hit DB directly
    s._get_customer = AsyncMock()
    s._get_customer_with_card = AsyncMock()
    s._get_card_by_card_id = AsyncMock()
    s._check_customer_has_card = AsyncMock()
    s._check_card_attached = AsyncMock()

    return s



# create_customer

@pytest.mark.asyncio
async def test_create_customer_ok_without_card(service):
    # DTO-like object: only attributes we need
    dto = SimpleNamespace(id=1, name="Alice", card=None)

    created_customer = SimpleNamespace(id=1, name="Alice", loyalty_card=None)
    service.repo.create_customer.return_value = created_customer
    service._get_customer_with_card.return_value = created_customer

    result = await service.create_customer(dto)

    service.repo.create_customer.assert_awaited_once_with(dto)
    assert result.id == 1
    assert result.name == "Alice"
    assert result.card is None


@pytest.mark.asyncio
async def test_create_customer_invalid_id_raises_bad_request(service):
    dto = SimpleNamespace(id=0, name="Zero", card=None)  # id <= 0 not allowed

    with pytest.raises(BadRequestError):
        await service.create_customer(dto)

    service.repo.create_customer.assert_not_called()


@pytest.mark.asyncio
async def test_create_customer_with_existing_card_raises_conflict(service):
    nested_card = SimpleNamespace(card_id="1234567890", points=10)
    dto = SimpleNamespace(id=1, name="Alice", card=nested_card)

    # card already exists
    service._get_card_by_card_id.return_value = SimpleNamespace(
        card_id="1234567890", points=10
    )

    with pytest.raises(ConflictError):
        await service.create_customer(dto)

    service.repo.create_customer.assert_not_called()


@pytest.mark.asyncio
async def test_create_customer_with_nested_card_success(service):
    nested_card = SimpleNamespace(card_id="1234567890", points=10)
    dto = SimpleNamespace(id=1, name="Alice", card=nested_card)

    # no existing card in DB
    service._get_card_by_card_id.return_value = None

    created_customer = SimpleNamespace(id=1, name="Alice", loyalty_card=None)
    service.repo.create_customer.return_value = created_customer

    created_card = SimpleNamespace(card_id="1234567890", points=10, customer_id=None)
    service.repo.create_card.return_value = created_card

    full_customer = SimpleNamespace(
        id=1,
        name="Alice",
        loyalty_card=SimpleNamespace(card_id="1234567890", points=10),
    )
    service._get_customer_with_card.return_value = full_customer

    result = await service.create_customer(dto)

    service.repo.create_customer.assert_awaited_once()
    service.repo.create_card.assert_awaited_once()
    service.repo.attach_card.assert_awaited_once_with(1, "1234567890")
    assert result.card is not None
    assert result.card.card_id == "1234567890"
    assert result.card.points == 10


# get_customer

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


# update_customer

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
async def test_update_customer_ok(service):
    dto = SimpleNamespace(name="New name", card=None)

    service._get_customer.return_value = SimpleNamespace(id=1)
    service.repo.update_customer.return_value = SimpleNamespace(id=1)
    full = SimpleNamespace(id=1, name="New name", loyalty_card=None)
    service._get_customer_with_card.return_value = full

    result = await service.update_customer(1, dto)

    service.repo.update_customer.assert_awaited_once_with(1, dto)
    assert result.name == "New name"


# delete_customer

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


# create_card

@pytest.mark.asyncio
async def test_create_card_negative_points_raises(service):
    dto = SimpleNamespace(card_id="1234567890", points=-1)

    with pytest.raises(BadRequestError):
        await service.create_card(dto)


@pytest.mark.asyncio
async def test_create_card_conflict(service):
    dto = SimpleNamespace(card_id="1234567890", points=0)
    service._get_card_by_card_id.return_value = SimpleNamespace(card_id="1234567890")

    with pytest.raises(ConflictError):
        await service.create_card(dto)


@pytest.mark.asyncio
async def test_create_card_ok(service):
    dto = SimpleNamespace(card_id="1234567890", points=5)
    service._get_card_by_card_id.return_value = None
    created = SimpleNamespace(card_id="1234567890", points=5)
    service.repo.create_card.return_value = created

    result = await service.create_card(dto)

    service.repo.create_card.assert_awaited_once_with(dto)
    assert result.card_id == "1234567890"
    assert result.points == 5


# attach_card & update_card_points

@pytest.mark.asyncio
async def test_attach_card_customer_already_has_card_raises(service):
    service._get_customer.return_value = SimpleNamespace(id=1)
    service._check_customer_has_card.side_effect = ConflictError("already has card")

    with pytest.raises(ConflictError):
        await service.attach_card(1, "1234567890")


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

