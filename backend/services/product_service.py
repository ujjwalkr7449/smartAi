from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.product import Product
from models.purchase_order import PurchaseOrderItem


def create_product(db: Session, payload):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_or_404(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def forecast_moving_average(db: Session, product_id: int) -> tuple[float, int]:
    product = get_product_or_404(db, product_id)
    rows = (
        db.query(PurchaseOrderItem.quantity)
        .filter(PurchaseOrderItem.product_id == product_id)
        .order_by(PurchaseOrderItem.id.desc())
        .limit(5)
        .all()
    )
    quantities = [r[0] for r in rows] or [max(product.threshold, 1)]
    avg = sum(quantities) / len(quantities)
    recommended = max(int(avg * 1.5) - product.stock, 0)
    return avg, recommended


def get_low_stock_products(db: Session):
    return db.query(Product).filter(Product.stock <= Product.threshold).all()
