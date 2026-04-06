from collections.abc import Generator
from typing import Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import Permission, RolePermission, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
    except JWTError as exc:
        raise auth_error from exc
    if not user_id:
        raise auth_error
    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise auth_error
    return user


def require_permission(module: str, action: Literal["view", "create", "edit", "delete"]):
    def checker(
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
    ) -> None:
        rows = (
            db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == current_user.role_id, Permission.module == module)
            .all()
        )
        if not rows:
            raise HTTPException(status_code=403, detail="No permission set for module")

        allowed = any(
            (action == "view" and p.can_view)
            or (action == "create" and p.can_create)
            or (action == "edit" and p.can_edit)
            or (action == "delete" and p.can_delete)
            for p in rows
        )
        if not allowed:
            raise HTTPException(status_code=403, detail="Insufficient permission")

    return checker
