from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import Product, ProductPrice, User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/price-history", dependencies=[Depends(require_permission("reports", "view"))])
def price_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = (
        db.query(Product.name, ProductPrice.date, ProductPrice.price)
        .join(Product, Product.id == ProductPrice.product_id)
        .filter(Product.company_id == current_user.company_id)
        .order_by(Product.name, ProductPrice.date)
        .all()
    )
    return [
        {"product_name": r[0], "date": r[1], "price": r[2]}
        for r in rows
    ]
