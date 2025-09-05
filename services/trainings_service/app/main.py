from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import trainings
from .core.config import get_settings
from .db.session import engine

settings = get_settings()


async def lifespan(app: FastAPI):
    yield
    try:
        engine.dispose()
    except Exception as exc:
        print(f"Engine dispose error: {exc}")


app = FastAPI(
    title="Trainings service",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.yaml",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    spec_path = Path(__file__).resolve().parent.parent / "docs" / "openapi.yaml"
    with open(spec_path, "r", encoding="utf-8") as fl:
        app.openapi_schema = yaml.safe_load(fl)

    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(trainings.router)
