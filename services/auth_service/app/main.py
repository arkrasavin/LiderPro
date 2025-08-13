from fastapi import FastAPI
from .routers import auth
from .core.config import get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
