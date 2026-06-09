from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.lib.templates import render_template
from app.lib.config import settings

router = APIRouter()


# NOTE: The "/" route is now handled by home_pages.py (Mako template).
# Auth routes start from /login onward.


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page():
    """Login page — email/password form + Google Sign-In button."""
    return render_template(
        "login.html",
        google_client_id=settings.GOOGLE_CLIENT_ID,
    )


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page():
    """Registration page — email/password form + Google Sign-Up button."""
    return render_template(
        "register.html",
        google_client_id=settings.GOOGLE_CLIENT_ID,
    )


@router.get("/create-account", response_class=HTMLResponse, include_in_schema=False)
async def create_account():
    return await register_page()
