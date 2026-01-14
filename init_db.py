from app.repositories.user_repository import UserRepository
from app.models.DTO.user_dto import UserDTO
from app.models.user_type import UserType
from app.database.database import reset_db, init_db as init_database
from passlib.context import CryptContext

from app.repositories.customer_repository import CustomerRepository
from app.models.DTO.customer_dto import CustomerCreateDTO, LoyaltyCardCreateDTO

from app.repositories.product_repository import ProductRepository
from app.models.DTO.product_dto import ProductCreateDTO

import asyncio
from app.controllers.auth_controller import pwd_context
from app.models.errors.notfound_error import NotFoundError

async def init_db():
    await init_database()

    user_repo = UserRepository()
    customer_repo = CustomerRepository()
    product_repo = ProductRepository()

    try:
        await user_repo.get_user_by_username("admin")
        print("Admin user already exists")
    except NotFoundError:
        await user_repo.create_user("admin", pwd_context.hash("admin"), UserType.Administrator)
        await user_repo.create_user("ShopManager", pwd_context.hash("ShManager"), UserType.ShopManager)
        await user_repo.create_user("Cashier", pwd_context.hash("Cashier"), UserType.Cashier)
        print("Admin/Manager/Cashier users created successfully")

    # Product
    existing_product = await product_repo.get_product_by_barcode("456789012345")
    if existing_product is None:
        product_dto = ProductCreateDTO(
            description="Mascara 30mL",
            barcode="456789012345",
            price_per_unit=1.80,
            note="Black Mascara",
            quantity=60,
            position="3-A-3",
        )
        await product_repo.create_product(product_dto)
        print("✅ Product created successfully")
    else:
        print("ℹ️ Product already exists")

async def reset():
    await reset_db()
    print("✅ Database reset successfully")
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    #loop.run_until_complete(reset()) 
    loop.run_until_complete(init_db())
