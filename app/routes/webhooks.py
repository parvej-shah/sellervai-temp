from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import logging

from app.lib.database import get_db
from app.models.models import Messenger, WhatsApp, Telegram, Instagram, ServiceStatus, Store
from app.services.message_processor import message_processor
import httpx

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.get("/messenger/{store_id}")
async def verify_messenger_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Verify Messenger webhook (Facebook verification)."""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    result = await db.execute(select(Store).filter(Store.id == store_id))
    store = result.scalar_one_or_none()

    if mode == "subscribe" and store and token == store.verification_token:
        logger.info(f"Messenger webhook verified for store {store_id}")
        return int(challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/messenger/{store_id}")
async def messenger_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming Messenger messages and events."""
    try:
        # Verify store and messenger config
        result = await db.execute(
            select(Messenger).filter(
                Messenger.store_id == store_id,
                Messenger.status == ServiceStatus.ACTIVE
            )
        )
        messenger = result.scalar_one_or_none()
        
        if not messenger:
            raise HTTPException(status_code=404, detail="Messenger not configured")
        
        # Parse webhook data
        data = await request.json()
        
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id")
                    
                    # Handle message
                    if messaging_event.get("message"):
                        message_text = messaging_event["message"].get("text", "")
                        
                        if message_text:
                            # Process message with AI
                            response = await message_processor.process_message(
                                platform="messenger",
                                store_id=str(store_id),
                                sender_id=sender_id,
                                message_text=message_text,
                                db=db
                            )
                            
                            # Send response back via Messenger API
                            await send_messenger_message(
                                messenger.page_id,
                                sender_id,
                                response,
                                messenger.api_key  # Access Token from DB
                            )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing Messenger webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def send_messenger_message(page_id: str, recipient_id: str, message: str, access_token: str):
    """Send a message via Messenger API."""
    url = f"https://graph.facebook.com/v18.0/me/messages"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    
    params = {
        "access_token": access_token
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, params=params)
        return response.json()


@router.get("/whatsapp/{store_id}")
async def verify_whatsapp_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Verify WhatsApp webhook."""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    result = await db.execute(select(Store).filter(Store.id == store_id))
    store = result.scalar_one_or_none()

    if mode == "subscribe" and store and token == store.verification_token:
        logger.info(f"WhatsApp webhook verified for store {store_id}")
        return int(challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp/{store_id}")
async def whatsapp_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming WhatsApp messages."""
    try:
        result = await db.execute(
            select(WhatsApp).filter(
                WhatsApp.store_id == store_id,
                WhatsApp.status == ServiceStatus.ACTIVE
            )
        )
        whatsapp = result.scalar_one_or_none()
        
        if not whatsapp:
            raise HTTPException(status_code=404, detail="WhatsApp not configured")
        
        data = await request.json()
        
        # Process WhatsApp webhook
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                for message in value.get("messages", []):
                    sender = message.get("from")
                    message_text = message.get("text", {}).get("body", "")
                    
                    if message_text:
                        # Process message with AI
                        response = await message_processor.process_message(
                            platform="whatsapp",
                            store_id=str(store_id),
                            sender_id=sender,
                            message_text=message_text,
                            db=db
                        )
                        
                        # Send response back via WhatsApp API
                        await send_whatsapp_message(
                            whatsapp.phone_number_id,
                            sender,
                            response,
                            whatsapp.api_key
                        )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def send_whatsapp_message(phone_number_id: str, recipient: str, message: str, access_token: str):
    """Send a message via WhatsApp Business API."""
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "text": {"body": message}
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()


# Telegram Webhook
@router.post("/telegram/{store_id}")
async def telegram_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming Telegram messages."""
    try:
        result = await db.execute(
            select(Telegram).filter(
                Telegram.store_id == store_id,
                Telegram.status == ServiceStatus.ACTIVE
            )
        )
        telegram = result.scalar_one_or_none()
        
        if not telegram:
            raise HTTPException(status_code=404, detail="Telegram not configured")
        
        data = await request.json()
        
        # Process Telegram update
        if "message" in data:
            message = data["message"]
            chat_id = message.get("chat", {}).get("id")
            message_text = message.get("text", "")
            
            if message_text:
                # Process message with AI
                response = await message_processor.process_message(
                    platform="telegram",
                    store_id=str(store_id),
                    sender_id=str(chat_id),
                    message_text=message_text,
                    db=db
                )
                
                # Send response back via Telegram API
                await send_telegram_message(
                    telegram.bot_token,
                    chat_id,
                    response
                )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def send_telegram_message(bot_token: str, chat_id: int, message: str):
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()


@router.get("/instagram/{store_id}")
async def verify_instagram_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Verify Instagram webhook."""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    result = await db.execute(select(Store).filter(Store.id == store_id))
    store = result.scalar_one_or_none()

    if mode == "subscribe" and store and token == store.verification_token:
        logger.info(f"Instagram webhook verified for store {store_id}")
        return int(challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/instagram/{store_id}")
async def instagram_webhook(
    store_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming Instagram messages and comments."""
    try:
        result = await db.execute(
            select(Instagram).filter(
                Instagram.store_id == store_id,
                Instagram.status == ServiceStatus.ACTIVE
            )
        )
        instagram = result.scalar_one_or_none()
        
        if not instagram:
            raise HTTPException(status_code=404, detail="Instagram not configured")
        
        data = await request.json()
        
        # Process Instagram webhook
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                
                # Handle message
                if messaging_event.get("message"):
                    message_text = messaging_event["message"].get("text", "")
                    
                    if message_text:
                        response = await message_processor.process_message(
                            platform="instagram",
                            store_id=str(store_id),
                            sender_id=sender_id,
                            message_text=message_text,
                            db=db
                        )
                        
                        # Send response (similar to Messenger API)
                        await send_instagram_message(
                            instagram.instagram_account_id,
                            sender_id,
                            response,
                            instagram.api_key
                        )
            
            # Handle comments
            for change in entry.get("changes", []):
                if change.get("field") == "comments":
                    value = change.get("value", {})
                    comment_text = value.get("text", "")
                    comment_id = value.get("id", "")
                    
                    if comment_text:
                        response = await message_processor.process_comment(
                            platform="instagram",
                            store_id=str(store_id),
                            post_id=value.get("media", {}).get("id", ""),
                            commenter_id=value.get("from", {}).get("id", ""),
                            comment_text=comment_text,
                            db=db
                        )
                        
                        # Reply to comment
                        await reply_instagram_comment(
                            comment_id,
                            response,
                            instagram.api_key
                        )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing Instagram webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def send_instagram_message(account_id: str, recipient_id: str, message: str, access_token: str):
    """Send a message via Instagram API."""
    url = f"https://graph.facebook.com/v18.0/me/messages"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    
    params = {"access_token": access_token}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, params=params)
        return response.json()


async def reply_instagram_comment(comment_id: str, message: str, access_token: str):
    """Reply to an Instagram comment."""
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    
    payload = {"message": message}
    params = {"access_token": access_token}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, params=params)
        return response.json()
