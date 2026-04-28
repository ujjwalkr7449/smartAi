from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from db.session import get_db
from models.purchase_order import PurchaseOrder
from schemas.purchase_order import PurchaseOrderCreateRequest, PurchaseOrderResponse, PurchaseOrderStatusUpdateRequest
from services.purchase_order_service import create_purchase_order, update_status

router = APIRouter()


@router.post("", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create(payload: PurchaseOrderCreateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_purchase_order(db, payload.supplier_id, payload.items, user.id)


@router.get("", response_model=list[PurchaseOrderResponse])
def list_pos(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(PurchaseOrder).all()


@router.patch("/{po_id}/status", response_model=PurchaseOrderResponse)
def change_status(po_id: int, payload: PurchaseOrderStatusUpdateRequest, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return update_status(db, po_id, payload.status)
