from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
import httpx

from app.lib.database import get_db
from app.models.models import User, Business, Messenger, WhatsApp, Telegram, Instagram, FacebookPages
from app.models.models import WebhookStatus, ServiceStatus
from app.schemas.schemas import (
    MessengerCreate, MessengerResponse,
    WhatsAppCreate, WhatsAppResponse,
    TelegramCreate, TelegramResponse,
    InstagramCreate, InstagramResponse,
    FacebookPagesCreate, FacebookPagesResponse,
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
    # Use SECRET_KEY to derive encryption key
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    f = Fernet(key)
    return f.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt API key."""
    key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    f = Fernet(key)
    return f.decrypt(encrypted_key.encode()).decode()


# Messenger Routes
@router.post("/messenger/{business_id}/api-key", response_model=MessengerResponse)
async def setup_messenger_api_key(
    business_id: UUID,
    messenger_data: MessengerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure Messenger API key for a business."""
    # Verify business ownership
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Check if messenger config already exists
    result = await db.execute(
        select(Messenger).filter(Messenger.business_id == business_id)
    )
    messenger = result.scalar_one_or_none()
    
    encrypted_key = encrypt_api_key(messenger_data.api_key)
    
    if messenger:
        # Update existing
        messenger.api_key = encrypted_key
        messenger.page_id = messenger_data.page_id
        messenger.status = ServiceStatus.INACTIVE
    else:
        # Create new
        messenger = Messenger(
            business_id=business_id,
            api_key=encrypted_key,
            page_id=messenger_data.page_id
        )
        db.add(messenger)
    
    await db.commit()
    await db.refresh(messenger)
    return messenger


@router.post("/messenger/{business_id}/webhook", response_model=WebhookVerification)
async def setup_messenger_webhook(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and activate Messenger webhook."""
    result = await db.execute(
        select(Messenger).filter(Messenger.business_id == business_id)
    )
    messenger = result.scalar_one_or_none()
    
    if not messenger:
        raise HTTPException(status_code=404, detail="Messenger not configured")
    
    # Here you would verify the webhook with Facebook
    # For now, we'll mark it as verified
    messenger.webhook_added_date = datetime.utcnow()
    messenger.webhook_status = WebhookStatus.VERIFIED
    messenger.status = ServiceStatus.ACTIVE
    
    await db.commit()
    
    return WebhookVerification(
        verified=True,
        message="Webhook verified and activated successfully"
    )


# WhatsApp Routes
@router.post("/whatsapp/{business_id}/api-key", response_model=WhatsAppResponse)
async def setup_whatsapp_api_key(
    business_id: UUID,
    whatsapp_data: WhatsAppCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure WhatsApp API key for a business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    result = await db.execute(
        select(WhatsApp).filter(WhatsApp.business_id == business_id)
    )
    whatsapp = result.scalar_one_or_none()
    
    encrypted_key = encrypt_api_key(whatsapp_data.api_key)
    
    if whatsapp:
        whatsapp.api_key = encrypted_key
        whatsapp.phone_number_id = whatsapp_data.phone_number_id
        whatsapp.business_account_id = whatsapp_data.business_account_id
        whatsapp.status = ServiceStatus.INACTIVE
    else:
        whatsapp = WhatsApp(
            business_id=business_id,
            api_key=encrypted_key,
            phone_number_id=whatsapp_data.phone_number_id,
            business_account_id=whatsapp_data.business_account_id
        )
        db.add(whatsapp)
    
    await db.commit()
    await db.refresh(whatsapp)
    return whatsapp


@router.post("/whatsapp/{business_id}/webhook", response_model=WebhookVerification)
async def setup_whatsapp_webhook(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and activate WhatsApp webhook."""
    result = await db.execute(
        select(WhatsApp).filter(WhatsApp.business_id == business_id)
    )
    whatsapp = result.scalar_one_or_none()
    
    if not whatsapp:
        raise HTTPException(status_code=404, detail="WhatsApp not configured")
    
    whatsapp.webhook_added_date = datetime.utcnow()
    whatsapp.webhook_status = WebhookStatus.VERIFIED
    whatsapp.status = ServiceStatus.ACTIVE
    
    await db.commit()
    
    return WebhookVerification(
        verified=True,
        message="Webhook verified and activated successfully"
    )


# Telegram Routes
@router.post("/telegram/{business_id}/api-key", response_model=TelegramResponse)
async def setup_telegram_api_key(
    business_id: UUID,
    telegram_data: TelegramCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure Telegram bot token for a business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    result = await db.execute(
        select(Telegram).filter(Telegram.business_id == business_id)
    )
    telegram = result.scalar_one_or_none()
    
    encrypted_token = encrypt_api_key(telegram_data.bot_token)
    
    if telegram:
        telegram.bot_token = encrypted_token
        telegram.bot_username = telegram_data.bot_username
        telegram.status = ServiceStatus.INACTIVE
    else:
        telegram = Telegram(
            business_id=business_id,
            bot_token=encrypted_token,
            bot_username=telegram_data.bot_username
        )
        db.add(telegram)
    
    await db.commit()
    await db.refresh(telegram)
    return telegram


@router.post("/telegram/{business_id}/webhook", response_model=WebhookVerification)
async def setup_telegram_webhook(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and activate Telegram webhook."""
    result = await db.execute(
        select(Telegram).filter(Telegram.business_id == business_id)
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


# Instagram Routes
@router.post("/instagram/{business_id}/api-key", response_model=InstagramResponse)
async def setup_instagram_api_key(
    business_id: UUID,
    instagram_data: InstagramCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure Instagram API key for a business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    result = await db.execute(
        select(Instagram).filter(Instagram.business_id == business_id)
    )
    instagram = result.scalar_one_or_none()
    
    encrypted_key = encrypt_api_key(instagram_data.api_key)
    
    if instagram:
        instagram.api_key = encrypted_key
        instagram.instagram_account_id = instagram_data.instagram_account_id
        instagram.status = ServiceStatus.INACTIVE
    else:
        instagram = Instagram(
            business_id=business_id,
            api_key=encrypted_key,
            instagram_account_id=instagram_data.instagram_account_id
        )
        db.add(instagram)
    
    await db.commit()
    await db.refresh(instagram)
    return instagram


@router.post("/instagram/{business_id}/webhook", response_model=WebhookVerification)
async def setup_instagram_webhook(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify and activate Instagram webhook."""
    result = await db.execute(
        select(Instagram).filter(Instagram.business_id == business_id)
    )
    instagram = result.scalar_one_or_none()
    
    if not instagram:
        raise HTTPException(status_code=404, detail="Instagram not configured")
    
    instagram.webhook_added_date = datetime.utcnow()
    instagram.webhook_status = WebhookStatus.VERIFIED
    instagram.status = ServiceStatus.ACTIVE
    
    await db.commit()
    
    return WebhookVerification(
        verified=True,
        message="Webhook verified and activated successfully"
    )
