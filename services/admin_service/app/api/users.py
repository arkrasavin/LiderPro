from fastapi import APIRouter, Depends

from ..core.deps import require_roles

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me/roles")
def me(payload=Depends(require_roles("admin", "observer", "participant"))):
    out_dict = {"roles": payload.roles, "effective": payload.role}

    return out_dict
