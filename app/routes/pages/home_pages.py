from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.lib.templates import render_template

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage():
    """Public landing page — rendered with Mako from templates/index.html."""
    return render_template("index.html")
