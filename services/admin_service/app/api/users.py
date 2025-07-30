from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.deps import require_role, get_db
from ..core.security import hash_password
from ..models.user import User

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))]
)
def create_user(payload: dict, db: Session = Depends(get_db)):
    """Создание нового пользователя (доступно только для admin)."""
    if db.scalar(select(User).where(User.email == payload["email"])):
        raise HTTPException(409, "Email exists")

    user = User(
        name=payload["name"],
        email=payload["email"],
        hasged_password=hash_password(payload["password"]),
        role=payload.get("role", "observer"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }


def list_users(db: Session = Depends(get_db)):
    """Список всех учетных записей (только admin)"""
    return db.scalars(select(User)).all()


def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удаление пользователя (только admin)"""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, f"User not found")
    db.delete(user)
    db.commit()
