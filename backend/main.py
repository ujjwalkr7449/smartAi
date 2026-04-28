from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.base import Base
from db.session import engine
from routers import ai, auth, health, products, purchase_orders, suppliers
from services.scheduler_service import scheduler_service
from utils.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    scheduler_service.start()
    yield
    scheduler_service.shutdown()


app = FastAPI(
    title="SmartStore AI API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
