import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace
from datetime import datetime

from app.repositories.return_repository import ReturnRepository
from app.models.return_status import ReturnStatus
from app.models.DAO.return_dao import ReturnDAO, ReturnLineDAO

@pytest.fixture
def repo():
    r = ReturnRepository()
    mock_session = AsyncMock()
    r._session = mock_session
    return r

@pytest.fixture
def mock_session():
    session = AsyncMock()
    # Mock context manager behavior (async with session...)
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    session.add = MagicMock()
    
    return session

@pytest.mark.asyncio
async def test_create_return(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.create_return(sale_id=10)
    
    assert result.sale_id == 10
    assert result.status == ReturnStatus.OPEN
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_return_found(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    # Mock DB result
    expected_return = SimpleNamespace(id=1, sale_id=10)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected_return
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_return(1)
    
    assert result.id == 1
    mock_session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_list_returns(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.list_returns()
    
    assert len(result) == 2

@pytest.mark.asyncio
async def test_delete_return_success(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    # Mock getting the return first
    mock_ret = SimpleNamespace(id=1)
    mock_session.get = AsyncMock(return_value=mock_ret)

    result = await repo.delete_return(1)
    
    assert result is True
    mock_session.delete.assert_awaited_once_with(mock_ret)
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_return_not_found(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    mock_session.get = AsyncMock(return_value=None)

    result = await repo.delete_return(999)
    
    assert result is False
    mock_session.delete.assert_not_awaited()

@pytest.mark.asyncio
async def test_add_item(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    result = await repo.add_item(return_id=1, barcode="ABC", quantity=1, price=10.0)
    
    assert result is True
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_remove_item_decrements_quantity(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    # Mock existing line with quantity 5
    line_mock = MagicMock()
    line_mock.quantity = 5
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = line_mock
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Remove 2
    await repo.remove_item(1, "ABC", 2)
    
    # Expect quantity to be 3
    assert line_mock.quantity == 3
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_remove_item_deletes_line_if_quantity_zero(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    line_mock = MagicMock()
    line_mock.quantity = 2
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = line_mock
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Remove 2 (or more)
    await repo.remove_item(1, "ABC", 2)
    
    mock_session.delete.assert_awaited_once_with(line_mock)

@pytest.mark.asyncio
async def test_close_return(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.OPEN
    mock_session.get = AsyncMock(return_value=mock_ret)

    await repo.close_return(1)
    
    assert mock_ret.status == ReturnStatus.CLOSED
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_reimburse_return(repo, mock_session):
    repo._get_session = AsyncMock(return_value=mock_session)
    
    mock_ret = MagicMock()
    mock_ret.status = ReturnStatus.CLOSED
    mock_session.get = AsyncMock(return_value=mock_ret)

    await repo.reimburse_return(1)
    
    assert mock_ret.status == ReturnStatus.REIMBURSED
    mock_session.commit.assert_awaited_once()