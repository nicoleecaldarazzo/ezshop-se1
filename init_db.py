#from app.controllers.auth_controller import get_password_hash

from app.repositories.user_repository import UserRepository
from app.models.DTO.user_dto import UserDTO
from app.models.user_type import UserType
from app.database.database import reset_db, init_db as init_database

from app.repositories.customer_repository import CustomerRepository
from app.models.DTO.customer_dto import CustomerCreateDTO, LoyaltyCardCreateDTO

from app.repositories.product_repository import ProductRepository
from app.models.DTO.product_dto import ProductCreateDTO

import asyncio

async def init_db():
    await init_database()

    user_repo = UserRepository()
    customer_repo = CustomerRepository()
    product_repo = ProductRepository()

    # Check if admin already exists
    try: 
        res = await user_repo.get_user_by_username("admin")
        if res is not None:
            print("ℹ️ Admin user already exists")
    except:
        admin_dto = UserDTO(username="admin", password="admin", type=UserType.Administrator)
        manager_dto = UserDTO(username="ShopManager", password="ShManager", type=UserType.ShopManager)
        cashier_dto = UserDTO(username="Cashier", password="Cashier", type=UserType.Cashier)
        await user_repo.create_user(admin_dto.username, admin_dto.password, admin_dto.type)
        await user_repo.create_user(manager_dto.username, manager_dto.password, manager_dto.type)
        await user_repo.create_user(cashier_dto.username, cashier_dto.password, cashier_dto.type)
        print("✅ Admin user created successfully")


    # Check if Customer already exists
    existing_customer = await customer_repo.get_customer_by_name("Mario Rossi")
    if existing_customer is None:
        customer_dto = CustomerCreateDTO(id=1, name="Mario Rossi")
        await customer_repo.create_customer(customer_dto)
        print("✅ Customer created successfully")
    else:
        print("ℹ️ Customer already exists")

    # Check if Product already exists
    existing_product = await product_repo.get_product_by_barcode("456789012345")
    if existing_product is None:
        product_dto = ProductCreateDTO(description="Mascara 30mL", 
            barcode="456789012345",
            price_per_unit=1.80,
            note="Black Mascara",
            quantity=60,
            position="3-A-3")
        await product_repo.create_product(product_dto)
        print("✅ Product created successfully")
    else:
        print("ℹ️ Product already exists")

async def reset():
    await reset_db()
    print("✅ Database reset successfully")
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_db())
    #loop.run_until_complete(reset())
