from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.deps import get_current_user, get_db
from ..models.user import User
from ..core.security import verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login")
def login(
        form: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(400, "Incorrect username or password")

    return {
        "access_token": create_access_token(str(user.id)),
        "token_type": "bearer",
    }


@router.get("/me")
def read_me(current=Depends(get_current_user)):
    """Информация о себе"""
    return {
        "id": current.id,
        "name": current.name,
        "email": current.email,
        "role": current.role,
    }
