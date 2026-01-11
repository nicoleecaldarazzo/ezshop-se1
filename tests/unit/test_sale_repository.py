import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from datetime import datetime, timezone

from app.repositories.sale_repository import SaleRepository
from app.models.sale_status import SaleStatus
from app.models.DAO.sale_dao import SaleDAO

@pytest.fixture
def repo():
    r = SaleRepository()
    mock_session = AsyncMock()
    r._session = mock_session
    return r

@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    session.add = MagicMock() # Sync method
    return session

@pytest.mark.asyncio
async def test_create_sale(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.create_sale()
    
    assert isinstance(result, SaleDAO)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_sale_found(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    expected_sale = SimpleNamespace(id=1)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected_sale
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_sale(1)
    assert result.id == 1

@pytest.mark.asyncio
async def test_add_line(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.add_line(1, "ABC", 5)
    
    assert result is True
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_remove_line_decrements(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_line = MagicMock()
    mock_line.quantity = 10
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_line
    mock_session.execute = AsyncMock(return_value=mock_result)

    await repo.remove_line(1, "ABC", 2)
    
    assert mock_line.quantity == 8
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_remove_line_deletes(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_line = MagicMock()
    mock_line.quantity = 2
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_line
    mock_session.execute = AsyncMock(return_value=mock_result)

    await repo.remove_line(1, "ABC", 5) # Remove more than exists
    
    mock_session.delete.assert_awaited_once_with(mock_line)

@pytest.mark.asyncio
async def test_set_discount(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_sale = MagicMock()
    mock_session.get = AsyncMock(return_value=mock_sale)

    await repo.set_discount(1, 0.2)
    
    assert mock_sale.discount_rate == 0.2
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_set_status_updates_timestamp(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_sale = MagicMock()
    mock_sale.closed_at = None # Not closed yet
    mock_session.get = AsyncMock(return_value=mock_sale)

    await repo.set_status(1, SaleStatus.PENDING)
    
    assert mock_sale.status == SaleStatus.PENDING
    assert mock_sale.closed_at is not None # Should be set now
