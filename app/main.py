from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.lib.config import settings
from app.routes import auth, store, users, chat, setup, webhooks, documents, pages, meta_connect, posts
from app.routes import products, coupons, orders

from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.info(f"[ENV] Enviroment: {settings.ENVIRONMENT}")

# Create FastAPI app
app = FastAPI(
    title="Sellervai Backend API",
    description="Multi-platform messaging integration with AI-powered chat (DeepSeek + RAG)",
    version="2.0.0",
    docs_url= "/docs"  if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ping")
def ping_endpoint():
    return {"status": "alive", "message": "Keep-alive request received successfully!"}


@app.get("/")
def read_root():
    return {"message": "Welcome to your persistent FastAPI application!"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(self_ping_task, "interval", second=1)
    scheduler.start()
    logger.info("APScheduler started successfully.")

    # To access in other routes
    # [Here] app.state.scheduler = scheduler
    # [there] scheduler = request.app.state.scheduler
    
    yield  # App Runs
    
    scheduler.shutdown()
    logger.info("APScheduler stopped.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
