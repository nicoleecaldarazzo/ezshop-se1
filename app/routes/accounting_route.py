from fastapi import APIRouter, Depends, status
from app.controllers.accounting_controller import AccountingController
from app.middleware.auth_middleware import authenticate_user
from app.models.user_type import UserType
from app.config.config import ROUTES

router = APIRouter(prefix=ROUTES["V1_BALANCE"], tags=["accounting"])
controller = AccountingController()

@router.get("", response_model=dict, dependencies=[Depends(authenticate_user([UserType.Administrator]))])
async def get_balance():
    balance = await controller.get_balance()
    return {"balance": balance}

@router.post("/set", status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate_user([UserType.Administrator]))])
async def set_balance(amount: float):
    success = await controller.set_balance(amount)
    return {"success": success}

@router.post("/reset", status_code=status.HTTP_205_RESET_CONTENT, dependencies=[Depends(authenticate_user([UserType.Administrator]))])
async def reset_balance():
    await controller.reset_balance()
    return