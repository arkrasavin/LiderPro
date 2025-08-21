from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import wallet
from .core.config import get_settings
from .db.session import engine

settings = get_settings()


async def lifespan(app: FastAPI):
    yield
    try:
        engine.dispose()
    except Exception as exc:
        print(f"Engine dispose error: {exc}")


app = FastAPI(title="Ewallet service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallet.router)
