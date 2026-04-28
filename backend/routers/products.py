from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from db.session import get_db
from models.product import Product
from schemas.product import ForecastResponse, ProductCreateRequest, ProductResponse, ProductUpdateRequest
from services.product_service import create_product, forecast_moving_average, get_product_or_404

router = APIRouter()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create(payload: ProductCreateRequest, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return create_product(db, payload)


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_product_or_404(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, payload: ProductUpdateRequest, db: Session = Depends(get_db), _=Depends(get_current_user)):
    product = get_product_or_404(db, product_id)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    product = get_product_or_404(db, product_id)
    db.delete(product)
    db.commit()
    return {"message": "Deleted"}


@router.get("/{product_id}/forecast", response_model=ForecastResponse)
def forecast(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    avg, recommended = forecast_moving_average(db, product_id)
    return ForecastResponse(product_id=product_id, moving_average_demand=avg, recommended_restock_quantity=recommended)
