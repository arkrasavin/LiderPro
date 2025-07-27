from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.session import get_current_user
from app.models.user import User
from app.models.employee_info import EmployeeInfo
from app.models.training import Training


router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="app/templates")


def get_employees_data(db: Session):
    employees_data = db.query(
        EmployeeInfo,
        Training
    ).outerjoin(
        Training,
        EmployeeInfo.id == Training.employee_id
    ).order_by(
        EmployeeInfo.name
    ).all()
    print(employees_data)

    employees = []
    for emp_info, edu_info in employees_data:
        employees.append({
            "employee": emp_info,
            "education": edu_info if edu_info else None
        })
    print(employees)
    return employees


@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    employees = get_employees_data(db=db)
    return templates.TemplateResponse("admin.html", {"request": request, "user": user, "employees": employees})