import pytest
import pytest_asyncio
import warnings
from sqlalchemy.exc import SAWarning
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.repositories.customer_repository import CustomerRepository
from app.models.DAO.customer_dao import CustomerDAO
from app.models.DAO.loyaltyCard_dao import LoyaltyCardDAO
from app.models.DTO.customer_dto import (
    CustomerCreateDTO,
    CustomerUpdateDTO,
    LoyaltyCardCreateDTO,
    LoyaltyCardUpdateDTO,
)
from app.models.errors.conflict_error import ConflictError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with SessionLocal() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def repo(async_session: AsyncSession):
    return CustomerRepository(session=async_session)


@pytest.mark.asyncio
async def test_create_customer_success(repo: CustomerRepository):
    dto = CustomerCreateDTO(id=1, name="Alice")
    customer = await repo.create_customer(dto)

    assert customer.id == 1
    assert customer.name == "Alice"

@pytest.mark.asyncio
async def test_create_customer_conflict(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))

    with pytest.raises(ConflictError):
        await repo.create_customer(CustomerCreateDTO(id=1, name="Bob"))

@pytest.mark.asyncio
async def test_get_customer_by_name_and_list(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    await repo.create_customer(CustomerCreateDTO(id=2, name="Bob"))

    by_name = await repo.get_customer_by_name("Bob")
    assert by_name is not None
    assert by_name.id == 2

    all_customers = await repo.list_customers()
    ids = sorted(c.id for c in all_customers)
    assert ids == [1, 2]

@pytest.mark.asyncio
async def test_delete_customer(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))

    assert await repo.delete_customer(1) is True
    assert await repo.delete_customer(1) is False


@pytest.mark.asyncio
async def test_update_customer_name_only(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))

    updated = await repo.update_customer(
        1, CustomerUpdateDTO(name="Alice Updated", card=None)
    )

    assert updated is not None
    assert updated.name == "Alice Updated"


@pytest.mark.asyncio
async def test_update_customer_detach_card(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=100))
    await repo.attach_card(customer_id=1, card_id="0000000001")

    empty_card = LoyaltyCardUpdateDTO(card_id=None, points=None)

    # FIX: Suppress the false-positive SAWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=SAWarning)
        updated = await repo.update_customer(
            1, CustomerUpdateDTO(name=None, card=empty_card)
        )

    assert updated is not None
    assert updated.loyalty_card is None


@pytest.mark.asyncio
async def test_update_customer_update_card_points(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=100))
    await repo.attach_card(customer_id=1, card_id="0000000001")

    card_update = LoyaltyCardUpdateDTO(card_id=None, points=250)

    updated = await repo.update_customer(
        1, CustomerUpdateDTO(name=None, card=card_update)
    )

    assert updated is not None
    assert updated.loyalty_card.points == 250

@pytest.mark.asyncio
async def test_update_customer_card_points_no_existing_card(repo, async_session):
    customer = CustomerDAO(id=1, name="Alice")
    async_session.add(customer)
    await async_session.commit()

    dto = CustomerUpdateDTO(
        name=None,
        card=LoyaltyCardUpdateDTO(card_id=None, points=100),
    )

    updated = await repo.update_customer(1, dto)

    assert updated is not None
    assert updated.id == 1
    assert updated.name == "Alice"
    assert updated.loyalty_card is None

@pytest.mark.asyncio
async def test_create_card_success(repo: CustomerRepository):
    card = await repo.create_card(
        LoyaltyCardCreateDTO(card_id="0000000001", points=50)
    )

    assert card.card_id == "0000000001"
    assert card.points == 50


@pytest.mark.asyncio
async def test_create_card_conflict(repo: CustomerRepository):
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=50))

    with pytest.raises(ConflictError):
        await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=0))

@pytest.mark.asyncio
async def test_attach_card_conflict_customer_already_has_card(repo, async_session):
    customer = CustomerDAO(id=1, name="Alice")
    card_attached = LoyaltyCardDAO(card_id="0000000001", points=10, customer_id=1)
    customer.loyalty_card = card_attached

    card_free = LoyaltyCardDAO(card_id="0000000002", points=5, customer_id=None)

    async_session.add_all([customer, card_attached, card_free])
    await async_session.commit()

    with pytest.raises(ConflictError):
        await repo.attach_card(1, "0000000002")


@pytest.mark.asyncio
async def test_attach_card_success(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=10))

    customer = await repo.attach_card(customer_id=1, card_id="0000000001")

    assert customer.loyalty_card.card_id == "0000000001"

@pytest.mark.asyncio
async def test_attach_card_conflicts(repo: CustomerRepository):
    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=10))
    await repo.attach_card(customer_id=1, card_id="0000000001")

    with pytest.raises(ConflictError):
        await repo.attach_card(customer_id=1, card_id="0000000001")

    await repo.create_customer(CustomerCreateDTO(id=2, name="Bob"))
    with pytest.raises(ConflictError):
        await repo.attach_card(customer_id=2, card_id="0000000001")

@pytest.mark.asyncio
async def test_attach_card_missing_customer_or_card(repo: CustomerRepository):
    res = await repo.attach_card(customer_id=999, card_id="0000000001")
    assert res is None

    await repo.create_customer(CustomerCreateDTO(id=1, name="Alice"))
    res2 = await repo.attach_card(customer_id=1, card_id="0000000001")
    assert res2 is None


@pytest.mark.asyncio
async def test_update_card_points_success(repo: CustomerRepository):
    await repo.create_card(LoyaltyCardCreateDTO(card_id="0000000001", points=10))

    updated = await repo.update_card_points("0000000001", 200)

    assert updated.points == 200

@pytest.mark.asyncio
async def test_update_card_points_not_found(repo: CustomerRepository):
    result = await repo.update_card_points("9999999999", 50)
    assert result is None