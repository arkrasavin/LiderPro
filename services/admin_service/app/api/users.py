from fastapi import APIRouter, Depends

from ..core.deps import require_roles

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def me(payload=Depends(require_roles("admin"))):
    out_dict = {
        "user_id": payload.sub,
        "email": payload.email,
        "role": payload.role
    }

    return out_dict
