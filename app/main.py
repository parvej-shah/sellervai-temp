from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import logging

from app.lib.config import settings
from app.routes import auth, store, users, chat, setup, webhooks, documents, pages, meta_connect, posts
from app.routes import products, coupons, orders

# from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"[ENV] Enviroment: {settings.ENVIRONMENT}")

async def self_ping_task():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get("http://localhost:8000/ping", timeout=5)
            logger.info(f"Self-ping: {r.status_code}")
        except Exception as e:
            logger.warning(f"Self-ping failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # scheduler = BackgroundScheduler()
    scheduler = AsyncIOScheduler()
    
    if settings.PLATFORM_IS_RENDER:
        scheduler.add_job(self_ping_task, "interval", minutes=10)

    scheduler.start()
    logger.info("APScheduler started successfully.")

    # To access in other routes
    # [Here] app.state.scheduler = scheduler
    # [there] scheduler = request.app.state.scheduler
    
    yield  # App Runs
    
    scheduler.shutdown()
    logger.info("APScheduler stopped.")

# Create FastAPI app
app = FastAPI(
    title="Sellervai Backend API",
    description="Multi-platform messaging integration with AI-powered chat (DeepSeek + RAG)",
    version="2.0.0",
    docs_url= "/docs"  if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(store.router)
app.include_router(documents.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(setup.router)
app.include_router(webhooks.router)
app.include_router(meta_connect.router)
app.include_router(products.router)
app.include_router(coupons.router)
app.include_router(orders.router)
app.include_router(posts.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/ping")
def ping_endpoint():
    return {"status": "alive", "message": "Keep-alive request received successfully!"}


@app.get("/")
def read_root():
    return {"message": "Welcome to your persistent FastAPI application!"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500,content={"detail": "Internal server error"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
