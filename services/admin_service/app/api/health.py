from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("", status_code=200)
def health():
    return {"status": "ok"}
