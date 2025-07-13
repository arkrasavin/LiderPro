from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from app.core.security import create_access_token, verify_password, get_password_hash
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.deps import get_db
from starlette.responses import HTMLResponse

templates = Jinja2Templates(directory="app/templates")
auth_router = APIRouter()

@auth_router.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    role = user.role
    if role == UserRole.admin:
        return RedirectResponse("/admin", status_code=303)
    elif role == UserRole.observer:
        return RedirectResponse("/observer", status_code=303)
    else:
        return RedirectResponse("/employee", status_code=303)

@auth_router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@auth_router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "User already exists"})
    user = User(username=username, hashed_password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)