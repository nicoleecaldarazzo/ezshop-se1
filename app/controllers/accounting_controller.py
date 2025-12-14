from app.repositories.system_repository import SystemRepository
from app.models.errors.bad_request import BadRequestError

class AccountingController:
    def __init__(self):
        self.repo = SystemRepository()

    async def get_balance(self) -> float:
        return await self.repo.get_balance()

    async def set_balance(self, amount: float) -> bool:
        if amount < 0:
            raise BadRequestError("Balance cannot be negative")
        await self.repo.set_balance(amount)
        return True

    async def reset_balance(self) -> None:
        await self.repo.set_balance(0.0)