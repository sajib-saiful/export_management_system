from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import Supplier, User
from app.schemas.common import SupplierCreate, SupplierOut

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("", response_model=list[SupplierOut], dependencies=[Depends(require_permission("suppliers", "view"))])
def list_suppliers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Supplier).filter(Supplier.company_id == current_user.company_id).all()


@router.post("", response_model=SupplierOut, dependencies=[Depends(require_permission("suppliers", "create"))])
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = Supplier(company_id=current_user.company_id, **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{row_id}", response_model=SupplierOut, dependencies=[Depends(require_permission("suppliers", "edit"))])
def update_supplier(row_id: int, payload: SupplierCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Supplier).filter(Supplier.id == row_id, Supplier.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump().items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{row_id}", dependencies=[Depends(require_permission("suppliers", "delete"))])
def delete_supplier(row_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Supplier).filter(Supplier.id == row_id, Supplier.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(row)
    db.commit()
    return {"message": "Deleted"}
