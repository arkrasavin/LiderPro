from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

dashboard_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@dashboard_router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@dashboard_router.get("/observer", response_class=HTMLResponse)
def observer_dashboard(request: Request):
    return templates.TemplateResponse("observer.html", {"request": request})

@dashboard_router.get("/employee", response_class=HTMLResponse)
def employee_dashboard(request: Request):
    return templates.TemplateResponse("employee.html", {"request": request})