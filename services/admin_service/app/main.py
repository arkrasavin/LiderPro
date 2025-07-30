from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, users
from .core.config import get_settings

app = FastAPI(title="HR Admin Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
