from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import CostHead, User
from app.schemas.common import CostHeadCreate, CostHeadOut

router = APIRouter(prefix="/cost-heads", tags=["Cost Heads"])


@router.get("", response_model=list[CostHeadOut], dependencies=[Depends(require_permission("cost_heads", "view"))])
def list_cost_heads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(CostHead).filter(CostHead.company_id == current_user.company_id).all()


@router.post("", response_model=CostHeadOut, dependencies=[Depends(require_permission("cost_heads", "create"))])
def create_cost_head(payload: CostHeadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    type_upper = payload.type.upper()
    if type_upper not in {"FOB", "CFR", "CPT"}:
        raise HTTPException(status_code=400, detail="Type must be FOB/CFR/CPT")
    row = CostHead(company_id=current_user.company_id, name=payload.name, type=type_upper, is_active=payload.is_active)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{row_id}", response_model=CostHeadOut, dependencies=[Depends(require_permission("cost_heads", "edit"))])
def update_cost_head(row_id: int, payload: CostHeadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(CostHead).filter(CostHead.id == row_id, CostHead.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    row.name = payload.name
    row.type = payload.type.upper()
    row.is_active = payload.is_active
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{row_id}", dependencies=[Depends(require_permission("cost_heads", "delete"))])
def delete_cost_head(row_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(CostHead).filter(CostHead.id == row_id, CostHead.company_id == current_user.company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(row)
    db.commit()
    return {"message": "Deleted"}
