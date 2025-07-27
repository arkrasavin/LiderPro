from datetime import datetime

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse

from app.core.session import get_current_user
from app.core.deps import get_db
from app.models.user import User
from app.models.employee_info import EmployeeInfo
from app.models.training import Training


dashboard_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_employees_data(db: Session):
    employees_data = db.query(
        EmployeeInfo,
        Training
    ).outerjoin(
        Training,
        EmployeeInfo.emp_ind == Training.emp_ind
    ).order_by(
        EmployeeInfo.name
    ).all()

    employees = []
    for emp_info, edu_info in employees_data:
        employees.append({
            "employee": emp_info,
            "education": edu_info if edu_info else None
        })

    return employees


# @dashboard_router.get("/admin", response_class=HTMLResponse)
# def admin_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     employees = get_employees_data(db=db)
#     return templates.TemplateResponse("admin.html", {"request": request, "user": user, "employees": employees})


@dashboard_router.get("/observer", response_class=HTMLResponse)
def observer_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    employees = get_employees_data(db=db)
    return templates.TemplateResponse("observer.html", {"request": request, "user": user, "employees": employees})

@dashboard_router.get("/employee", response_class=HTMLResponse)
def employee_dashboard(request: Request, db: Session = Depends(get_db), current_user_data: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.login == current_user_data["login"]).first()
    return templates.TemplateResponse("employee.html", {"request": request, "user": user})