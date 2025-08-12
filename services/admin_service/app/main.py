from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import users, health
from .core.config import get_settings

app = FastAPI(title="Admin service")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(users.router)
