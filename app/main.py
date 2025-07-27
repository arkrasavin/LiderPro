from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.routes import auth_router
from app.api.routes import dashboard_router
from app.api.employee_routes import router as employee_router

from app.api import router

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(router)


from app.core.database import engine
from app.models.user import Base as UserBase

UserBase.metadata.create_all(bind=engine)
app.include_router(employee_router)
