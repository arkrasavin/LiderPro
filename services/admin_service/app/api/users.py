from fastapi import APIRouter, Depends

from ..core.deps import require_roles
from shared_schemas.security import TokenPayload

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me")
def me(payload: TokenPayload = Depends(require_roles("admin", "observer"))):
    return {
        "user_id": payload.sub,
        "email": payload.email,
        "role": payload.role,
    }
