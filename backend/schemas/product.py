from datetime import date

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    sku: str
    stock: int = Field(ge=0)
    price: float = Field(gt=0)
    expiry: date | None = None
    threshold: int = Field(ge=0)


class ProductUpdateRequest(BaseModel):
    name: str | None = None
    stock: int | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, gt=0)
    expiry: date | None = None
    threshold: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    stock: int
    price: float
    expiry: date | None
    threshold: int

    model_config = {"from_attributes": True}


class ForecastResponse(BaseModel):
    product_id: int
    moving_average_demand: float
    recommended_restock_quantity: int
