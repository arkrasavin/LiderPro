from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, Response, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from shared_schemas.users import UserCreate
from shared_schemas.auth import Token, PasswordResetRequest, PasswordResetConfirm
from ..core.deps import get_db_session
from ..core.email import send_email
from ..models.user import User, PasswordResetToken
from ..core.security import get_password_hash, verify_password, create_access_token

ACCESS_TOKEN_TTL = timedelta(minutes=60)

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db_session)):
    """
    Регистрация нового пользователя.
    """
    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email exists")
    user = User(
        name=payload.name,
        email=payload.email.lower(),
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=Token)
def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_session),
):
    """
    Аутентификация пользователя, создание JWT токена. Установка cookie.
    """
    user = db.query(User).filter(User.email == form_data.username.lower()).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Incorrect username or password")
    token = create_access_token(
        {"sub": str(user.id), "role": user.role},
        expires_delta=ACCESS_TOKEN_TTL
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return Token(access_token=token, token_type="bearer")


@router.get("/password/reset")
def request_reset(
        req: PasswordResetRequest,
        tasks: BackgroundTasks,
        db: Session = Depends(get_db_session)
):
    """
    Запрос на сброс пароля, отправка ссылки на почту.
    """
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user:
        return {"message": "If email exists, reset link will be sent."}
    token = PasswordResetToken(
        user_id=user.id,
        token=str(int(datetime.now(timezone.utc).timestamp())),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        used=False,
    )
    db.add(token)
    db.commit()
    reset_link = f"{req.base_url}/reset?token={token.token}"
    tasks.add_task(send_email, to=user.email, subject="Password reset", body=reset_link)

    return {"message": "Reset link sent."}


@router.post("/password/confirm")
def confirm_reset(
        req: PasswordResetConfirm,
        db: Session = Depends(get_db_session)
):
    """
    Подтверждение сброса пароля и его обновление.
    """
    rec = db.query(
        PasswordResetToken).filter(
        PasswordResetToken.token == req.token
    ).first()
    if not rec or rec.used or rec.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Invalid or expired token")

    user = db.get(User, rec.user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.hashed_password = get_password_hash(req.new_password)
    rec.used = True
    db.commit()

    return {"message": "Password updated successfully"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    """
    Выход пользователя, удаление cookie.
    """
    response.delete_cookie("access_token", samesite="lax")

    return
