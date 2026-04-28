from datetime import datetime

from pydantic import BaseModel

from models.purchase_order import PurchaseOrderStatus


class PurchaseOrderItemCreateRequest(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class PurchaseOrderCreateRequest(BaseModel):
    supplier_id: int
    items: list[PurchaseOrderItemCreateRequest]


class PurchaseOrderStatusUpdateRequest(BaseModel):
    status: PurchaseOrderStatus


class PurchaseOrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    status: PurchaseOrderStatus
    total_amount: float
    created_by: int
    created_at: datetime
    items: list[PurchaseOrderItemResponse]

    model_config = {"from_attributes": True}
