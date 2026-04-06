from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.models import Calculation, CostEntry, User
from app.schemas.common import CalculationCreate, CalculationOut
from app.services.calculation_service import create_calculation

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.post("", response_model=CalculationOut, dependencies=[Depends(require_permission("calculations", "create"))])
def create_calc(payload: CalculationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_calculation(db, current_user, payload)


@router.get("", response_model=list[CalculationOut], dependencies=[Depends(require_permission("calculations", "view"))])
def list_calculations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Calculation)
        .filter(Calculation.company_id == current_user.company_id)
        .order_by(Calculation.id.desc())
        .all()
    )


@router.get("/{calc_id}", dependencies=[Depends(require_permission("calculations", "view"))])
def calculation_detail(calc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.company_id == current_user.company_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")
    entries = db.query(CostEntry).filter(CostEntry.calculation_id == calc.id).all()
    return {
        "calculation": calc,
        "entries": entries,
    }
