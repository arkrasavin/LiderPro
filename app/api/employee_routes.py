from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.session import get_current_user
from app.core.deps import get_db
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/employee", response_class=HTMLResponse)
def employee_dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("employee.html", {"request": request, "user": user.username})

# @router.post("/checkin")
# def check_in(request: Request, db: Session = Depends(get_db)):
#     user_data = get_current_user(request)
#     if not user_data:
#         return RedirectResponse("/", status_code=302)
#     user = db.query(User).filter(User.login == user_data["login"]).first()
#     open_entry = db.query(TimeEntry).filter(TimeEntry.user_id == user.id, TimeEntry.check_out == None).first()
#     if open_entry:
#         return RedirectResponse("/employee", status_code=302)
#     entry = TimeEntry(user_id=user.id)
#     db.add(entry)
#     db.commit()
#     return RedirectResponse("/employee", status_code=302)
#
# @router.post("/checkout")
# def check_out(request: Request, db: Session = Depends(get_db)):
#     user_data = get_current_user(request)
#     if not user_data:
#         return RedirectResponse("/", status_code=302)
#     user = db.query(User).filter(User.login == user_data["login"]).first()
#     entry = db.query(TimeEntry).filter(TimeEntry.user_id == user.id, TimeEntry.check_out == None).first()
#     if entry:
#         entry.check_out = datetime.utcnow()
#         db.commit()
#     return RedirectResponse("/employee", status_code=302)

@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(get_db)):
    user_data = get_current_user(request)
    if not user_data:
        return RedirectResponse("/", status_code=302)
    user = db.query(User).filter(User.username == user_data["username"]).first()
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})