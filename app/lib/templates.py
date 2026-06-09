"""
Mako template rendering helper.

Usage in a route:
    from app.lib.templates import render_template
    from fastapi.responses import HTMLResponse

    @router.get("/", response_class=HTMLResponse)
    async def homepage():
        return render_template("index.html", title="Home")
"""

from mako.lookup import TemplateLookup
from fastapi.responses import HTMLResponse
import os

# Resolve templates directory relative to the project root
_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "templates")

lookup = TemplateLookup(
    directories=[_BASE_DIR],
    module_directory="/tmp/mako_modules",  # compiled template cache
    input_encoding="utf-8",
    output_encoding="utf-8",
    encoding_errors="replace",
    strict_undefined=False,
)


def render_template(template_name: str, **context) -> HTMLResponse:
    """Render a Mako template file and return an HTMLResponse."""
    tmpl = lookup.get_template(template_name)
    html = tmpl.render(**context)
    # mako returns bytes when output_encoding is set
    if isinstance(html, bytes):
        html = html.decode("utf-8")
    return HTMLResponse(content=html)
