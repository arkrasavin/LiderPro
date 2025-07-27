from fastapi import APIRouter

from .admin.views import router as admin_router

router = APIRouter()
router.include_router(router=admin_router, prefix="/api/users")
