from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import Buyer, User
from app.schemas.common import BuyerCreate, BuyerOut

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.get("", response_model=list[BuyerOut], dependencies=[Depends(require_permission("buyers", "view"))])
def list_buyers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Buyer).filter(Buyer.company_id == current_user.company_id).all()


@router.post("", response_model=BuyerOut, dependencies=[Depends(require_permission("buyers", "create"))])
def create_buyer(payload: BuyerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = Buyer(company_id=current_user.company_id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{row_id}", response_model=BuyerOut, dependencies=[Depends(require_permission("buyers", "edit"))])
def update_buyer(row_id: int, payload: BuyerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Buyer).filter(Buyer.id == row_id, Buyer.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump().items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{row_id}", dependencies=[Depends(require_permission("buyers", "delete"))])
def delete_buyer(row_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Buyer).filter(Buyer.id == row_id, Buyer.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(row)
    db.commit()
    return {"message": "Deleted"}
