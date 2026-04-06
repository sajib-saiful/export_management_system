from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import Company, CostHead, Role, User
from app.schemas.common import LoginRequest, RegisterRequest


def register_company_admin(db: Session, payload: RegisterRequest) -> dict:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.name == "Admin").first()
    if not role:
        raise HTTPException(status_code=500, detail="Admin role not seeded")

    company = Company(name=payload.company_name)
    db.add(company)
    db.flush()

    user = User(
        company_id=company.id,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role_id=role.id,
        is_active=True,
    )
    db.add(user)
    db.flush()

    db.add_all(
        [
            CostHead(company_id=company.id, name="Packing", type="FOB", is_active=True),
            CostHead(company_id=company.id, name="Transport", type="FOB", is_active=True),
            CostHead(company_id=company.id, name="Shipping", type="CFR", is_active=True),
            CostHead(company_id=company.id, name="Air Freight", type="CPT", is_active=True),
        ]
    )
    db.commit()
    db.refresh(user)

    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}


def login(db: Session, payload: LoginRequest) -> dict:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
