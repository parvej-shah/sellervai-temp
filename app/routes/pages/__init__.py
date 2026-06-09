from fastapi import APIRouter

from .home_pages import router as home_router
from .auth_pages import router as auth_router
from .dashboard_pages import router as dashboard_router
from .store_pages import router as store_router
from .store_post_management import router as post_management_router

router = APIRouter()

# home_pages owns "/" — must be registered first
router.include_router(home_router)
router.include_router(auth_router)
router.include_router(dashboard_router)
router.include_router(store_router)
router.include_router(post_management_router)

__all__ = ["router"]
