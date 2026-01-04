import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.DTO.user_dto import UserDTO
from app.controllers.user_controller import UserController

@pytest.mark.asyncio
async def test_create_user_success():
    # Input data - Use "Cashier"
    input_dto = UserDTO(username="luigi", password="password123", type="Cashier")
    
    
    fake_created_user = MagicMock()
    fake_created_user.id = 1
    fake_created_user.username = "luigi"
    fake_created_user.type = "Cashier"

   
    with patch("app.controllers.user_controller.UserRepository") as MockRepoClass, \
         patch("app.controllers.user_controller.pwd_context") as mock_pwd_context:
        
        mock_repo_instance = MockRepoClass.return_value
        mock_repo_instance.create_user = AsyncMock(return_value=fake_created_user)
        
        mock_pwd_context.hash.return_value = "hashed_password_fake"

        
        controller = UserController()
        
    
        result = await controller.create_user(input_dto)

        
        assert result.username == "luigi"
      
        mock_repo_instance.create_user.assert_called_with("luigi", "hashed_password_fake", "Cashier")