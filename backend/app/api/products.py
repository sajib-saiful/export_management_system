from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import Product, ProductPrice, User
from app.schemas.common import ProductCreate, ProductOut, ProductPriceCreate, ProductPriceOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductOut], dependencies=[Depends(require_permission("products", "view"))])
def list_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Product).filter(Product.company_id == current_user.company_id).all()


@router.post("", response_model=ProductOut, dependencies=[Depends(require_permission("products", "create"))])
def create_product(payload: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = Product(company_id=current_user.company_id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_permission("products", "edit"))])
def update_product(product_id: int, payload: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Product).filter(Product.id == product_id, Product.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump().items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{product_id}", dependencies=[Depends(require_permission("products", "delete"))])
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Product).filter(Product.id == product_id, Product.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(row)
    db.commit()
    return {"message": "Deleted"}


@router.post("/price-history", response_model=ProductPriceOut, dependencies=[Depends(require_permission("products", "create"))])
def create_price_history(payload: ProductPriceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id, Product.company_id == current_user.company_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    row = ProductPrice(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
