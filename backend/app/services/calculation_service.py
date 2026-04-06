from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Calculation, CostEntry, CostHead, Product, User
from app.schemas.common import CalculationCreate


def create_calculation(db: Session, current_user: User, payload: CalculationCreate) -> Calculation:
    product = (
        db.query(Product)
        .filter(Product.id == payload.product_id, Product.company_id == current_user.company_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    head_ids = [entry.cost_head_id for entry in payload.entries]
    heads = (
        db.query(CostHead)
        .filter(CostHead.company_id == current_user.company_id, CostHead.id.in_(head_ids))
        .all()
    )
    head_map = {h.id: h for h in heads}
    if len(head_map) != len(set(head_ids)):
        raise HTTPException(status_code=400, detail="Some cost heads are invalid")

    sums = defaultdict(float)
    for item in payload.entries:
        sums[head_map[item.cost_head_id].type] += item.amount

    total_fob = sums["FOB"]
    total_cfr = total_fob + sums["CFR"]
    total_cpt = total_fob + sums["CPT"]

    calc = Calculation(
        company_id=current_user.company_id,
        product_id=payload.product_id,
        total_fob=total_fob,
        total_cfr=total_cfr,
        total_cpt=total_cpt,
    )
    db.add(calc)
    db.flush()

    db.add_all(
        [
            CostEntry(
                calculation_id=calc.id, cost_head_id=item.cost_head_id, amount=item.amount
            )
            for item in payload.entries
        ]
    )
    db.commit()
    db.refresh(calc)
    return calc
