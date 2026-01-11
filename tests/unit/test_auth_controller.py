import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.DTO.user_dto import UserDTO
from app.controllers.auth_controller import get_token
from app.models.errors.notfound_error import NotFoundError
from app.models.errors.unauthorized_error import UnauthorizedError

@pytest.mark.asyncio
async def test_get_token_success():
    # 1. ARRANGE - Use "Cashier" 
    fake_user_dto = UserDTO(username="mario", password="password123", type="Cashier")
    
    fake_user_dao = MagicMock()
    fake_user_dao.username = "mario"
    fake_user_dao.password = "hashed_secret_password"
    fake_user_dao.type = "Cashier"

    # 2. PATCH
    with patch("app.controllers.auth_controller.UserRepository") as MockRepoClass, \
         patch("app.controllers.auth_controller.pwd_context") as mock_pwd_context, \
         patch("app.controllers.auth_controller.generate_token") as mock_generate:

        mock_repo_instance = MockRepoClass.return_value
        mock_repo_instance.get_user_by_username = AsyncMock(return_value=fake_user_dao)

        mock_pwd_context.verify.return_value = True
        mock_generate.return_value = "fake_access_token_123"

        # 3. ACT
        result = await get_token(fake_user_dto)

        # 4. ASSERT
        assert result.token == "fake_access_token_123"
        mock_pwd_context.verify.assert_called_once()

@pytest.mark.asyncio
async def test_get_token_user_not_found():
    # Use "Administrator"
    fake_user_dto = UserDTO(username="fantasma", password="pwd", type="Administrator")

    with patch("app.controllers.auth_controller.UserRepository") as MockRepoClass:
        mock_repo_instance = MockRepoClass.return_value
        mock_repo_instance.get_user_by_username = AsyncMock(side_effect=NotFoundError("Entity not found"))

        with pytest.raises(NotFoundError):
            await get_token(fake_user_dto)

@pytest.mark.asyncio
async def test_get_token_wrong_password():
    # Use "Administrator"
    fake_user_dto = UserDTO(username="mario", password="sbagliata", type="Administrator")
    fake_user_dao = MagicMock()
    fake_user_dao.password = "real_hash"

    with patch("app.controllers.auth_controller.UserRepository") as MockRepoClass, \
         patch("app.controllers.auth_controller.pwd_context") as mock_pwd_context:
        
        mock_repo_instance = MockRepoClass.return_value
        mock_repo_instance.get_user_by_username = AsyncMock(return_value=fake_user_dao)
        
        mock_pwd_context.verify.return_value = False

        with pytest.raises(UnauthorizedError):
            await get_token(fake_user_dto)