from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models.product import Product
from models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from models.supplier import Supplier

ALLOWED_TRANSITIONS = {
    PurchaseOrderStatus.DRAFT: {PurchaseOrderStatus.SENT},
    PurchaseOrderStatus.SENT: {PurchaseOrderStatus.ACKNOWLEDGED},
    PurchaseOrderStatus.ACKNOWLEDGED: {PurchaseOrderStatus.RECEIVED},
    PurchaseOrderStatus.RECEIVED: set(),
}


def create_purchase_order(db: Session, supplier_id: int, items: list, user_id: int):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    po_items = []
    total = 0.0
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {item.product_id} not found")
        line_total = item.quantity * item.unit_price
        total += line_total
        po_items.append(PurchaseOrderItem(product_id=item.product_id, quantity=item.quantity, unit_price=item.unit_price))

    po = PurchaseOrder(supplier_id=supplier_id, created_by=user_id, total_amount=total, items=po_items)
    db.add(po)
    db.commit()
    db.refresh(po)
    return po


def update_status(db: Session, po_id: int, new_status: PurchaseOrderStatus):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    if new_status not in ALLOWED_TRANSITIONS[po.status]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid status transition")
    po.status = new_status
    db.commit()
    db.refresh(po)
    return po


def list_po_history(db: Session, product_id: int):
    return (
        db.query(PurchaseOrder)
        .options(joinedload(PurchaseOrder.items))
        .join(PurchaseOrder.items)
        .filter(PurchaseOrderItem.product_id == product_id)
        .order_by(PurchaseOrder.created_at.desc())
        .all()
    )
