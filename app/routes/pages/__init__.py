from fastapi import APIRouter

from .auth_pages import router as auth_router
from .dashboard_pages import router as dashboard_router
from .store_pages import router as store_router
from app.lib.config import settings

router = APIRouter()

# if settings.ENVIRONMENT == "development":
router.include_router(auth_router)
router.include_router(dashboard_router)
router.include_router(store_router)

__all__ = ["router"]
