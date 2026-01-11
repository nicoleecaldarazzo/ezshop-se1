import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.repositories.system_repository import SystemRepository
from app.models.DAO.system_dao import SystemInfoDAO

@pytest.fixture
def repo():
    SystemRepository._instance = None
    r = SystemRepository()
    mock_session = AsyncMock()
    r._session = mock_session
    return r

@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    session.add = MagicMock()
    return session

@pytest.mark.asyncio
async def test_get_singleton_creates_if_missing(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    # First query returns None (no row in DB)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_singleton()
    
    assert isinstance(result, SystemInfoDAO)
    assert result.balance == 0.0
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_balance(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_info = SimpleNamespace(balance=150.0)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_info
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_balance()
    assert result == 150.0

@pytest.mark.asyncio
async def test_set_balance(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_info = MagicMock()
    mock_info.balance = 50.0
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_info
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.set_balance(200.0)
    
    assert mock_info.balance == 200.0
    assert result == 200.0

@pytest.mark.asyncio
async def test_update_balance(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_info = MagicMock()
    mock_info.balance = 100.0
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_info
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Add 50
    result = await repo.update_balance(50.0)
    
    assert mock_info.balance == 150.0
    assert result == 150.0
