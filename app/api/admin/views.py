from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.session import get_current_user
from app.models.user import User

from app.api.admin.crud import get_employees_data


router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    employees = get_employees_data(db=db)
    return templates.TemplateResponse("admin.html", {"request": request, "user": user, "employees": employees})