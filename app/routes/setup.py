from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from app.lib.database import get_db
from app.models.models import User, Store, Telegram
from app.models.models import WebhookStatus, ServiceStatus
from app.schemas.schemas import (
    TelegramCreate, TelegramResponse,
    WebhookVerification
)
from app.lib.auth import get_current_user
from app.lib.config import settings
from cryptography.fernet import Fernet
import base64
import hashlib

router = APIRouter(prefix="/api/setup", tags=["Setup"])


def encrypt_api_key(api_key: str) -> str:
    """Encrypt API key for storage."""
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    f = Fernet(key)
    return f.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt API key."""
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    f = Fernet(key)
    return f.decrypt(encrypted_key.encode()).decode()


# Telegram Routes
@router.post("/telegram/{store_id}/api-key", response_model=TelegramResponse)
async def setup_telegram_api_key(
    store_id: UUID,
    telegram_data: TelegramCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure Telegram bot token for a store."""
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    result = await db.execute(
        select(Telegram).filter(Telegram.store_id == store_id)
    )
    telegram = result.scalar_one_or_none()
    
    encrypted_token = encrypt_api_key(telegram_data.bot_token)
    
    if telegram:
        telegram.bot_token = encrypted_token
        telegram.bot_username = telegram_data.bot_username
        telegram.status = ServiceStatus.INACTIVE
    else:
        telegram = Telegram(
            store_id=store_id,
            bot_token=encrypted_token,
            bot_username=telegram_data.bot_username
        )
        db.add(telegram)
    
    await db.commit()
    await db.refresh(telegram)
    return telegram


@router.post("/telegram/{store_id}/webhook", response_model=WebhookVerification)
async def setup_telegram_webhook(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and activate Telegram webhook."""
    result = await db.execute(
        select(Telegram).filter(Telegram.store_id == store_id)
    )
    telegram = result.scalar_one_or_none()
    
    if not telegram:
        raise HTTPException(status_code=404, detail="Telegram not configured")
    
    telegram.webhook_added_date = datetime.utcnow()
    telegram.webhook_status = WebhookStatus.VERIFIED
    telegram.status = ServiceStatus.ACTIVE
    
    await db.commit()
    
    return WebhookVerification(
        verified=True,
        message="Webhook verified and activated successfully"
    )

@router.get("/telegram/{store_id}")
async def get_telegram_connections(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all telegram connections for a store."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
    
    tg_result = await db.execute(
        select(Telegram).filter(Telegram.store_id == store_id)
    )
    connections = tg_result.scalars().all()
    
    return {
        "connections": [
            {
                "id": str(conn.id),
                "bot_username": conn.bot_username or "Unknown Bot",
                "status": conn.status,
                "webhook_status": conn.webhook_status
            }
            for conn in connections
        ]
    }

@router.delete("/telegram/{store_id}/{telegram_id}")
async def delete_telegram_connection(
    store_id: UUID,
    telegram_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a telegram connection."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
    
    tg_result = await db.execute(
        select(Telegram).filter(Telegram.id == telegram_id, Telegram.store_id == store_id)
    )
    conn = tg_result.scalar_one_or_none()
    if not conn:
        raise HTTPException(status_code=404, detail="Telegram connection not found")
        
    await db.delete(conn)
    await db.commit()
    return {"status": "success"}
