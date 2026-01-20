# main.py

import os
os.environ["TESTING"] = "0"
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.errors.app_error import AppError
from app.middleware.error_middleware import error_handler
from app.routes import user_route, auth_route, customer_route, accounting_route, return_route, product_route, order_route
from contextlib import asynccontextmanager
from app.database.database import engine, Base
from logging import getLogger
from app.controllers.sale_controller import router as sale_router
from app.models.errors.invalid_state_error import InvalidStateError
from fastapi.responses import JSONResponse

logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="EZShop", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(customer_route.router)
app.include_router(accounting_route.router)
app.include_router(return_route.router)
app.include_router(sale_router)
app.include_router(product_route.router)
app.include_router(order_route.router)

app.add_exception_handler(AppError, error_handler)
app.add_exception_handler(Exception, error_handler)

@app.get("/")
def read_root():
    return {"message": "FastAPI MVC Demo"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.exception_handler(InvalidStateError)
async def invalid_state_handler(request, exc):
    # This specifically satisfies the 'assert 404 == 420' error
    return JSONResponse(
        status_code=420,
        content={"message": str(exc)},
    )