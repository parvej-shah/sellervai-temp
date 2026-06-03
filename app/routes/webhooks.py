from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import logging
import httpx

from app.lib.database import get_db, AsyncSessionLocal
from app.models.models import ConnectedPage, ConnectedWhatsapp, ConnectedInstagram, Telegram, ServiceStatus, Store, Conversation, Message
from app.services.message_processor import message_processor
from app.lib.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.get("/meta")
async def verify_meta_webhook(request: Request):
    """Verify Meta (Messenger, Instagram, WhatsApp) webhook."""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # The verification token is defined globally in the app dashboard
    # Use settings.META_VERIFY_TOKEN or a hardcoded value if not present
    expected_token = getattr(settings, "META_VERIFY_TOKEN", "sellervai_meta_webhook_token")
    print("mode", mode)
    print("token", token)
    print("challenge", challenge)
    print("expected_token", expected_token)

    if mode == "subscribe" and token == expected_token:
        logger.info("Meta webhook verified")
        return int(challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/meta")
async def meta_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming Meta messages and events."""
    data = await request.json()
    logger.info(f"Received Meta webhook data: {data}")
    
    # Respond 200 immediately
    background_tasks.add_task(process_meta_webhook, data)
    
    return Response(content="EVENT_RECEIVED", status_code=200)


async def process_meta_webhook(data: dict):
    async with AsyncSessionLocal() as db:
        try:
            object_type = data.get("object")
            
            if object_type in ("page", "instagram"):
                for entry in data.get("entry", []):
                    entry_id = entry.get("id")
                    
                    platform = None
                    store_id = None
                    access_token = None
                    
                    if object_type == "page":
                        result = await db.execute(select(ConnectedPage).filter(ConnectedPage.page_id == entry_id))
                        page = result.scalar_one_or_none()
                        if not page:
                            continue
                        platform = "messenger"
                        store_id = page.store_id
                        access_token = page.token
                    else:
                        result = await db.execute(select(ConnectedInstagram).filter(ConnectedInstagram.ig_user_id == entry_id))
                        ig = result.scalar_one_or_none()
                        if not ig:
                            continue
                        platform = "instagram"
                        store_id = ig.store_id
                        # Instagram uses the Page Token or its own token
                        access_token = ig.token
                        if not access_token:
                            # Fallback to connected page token
                            p_res = await db.execute(select(ConnectedPage).filter(ConnectedPage.store_id == store_id))
                            p = p_res.scalar_one_or_none()
                            if p:
                                access_token = p.token

                    if not access_token:
                        logger.error(f"No access token found for {platform} store {store_id}")
                        continue
                        
                    for messaging_event in entry.get("messaging", []):
                        sender_id = messaging_event.get("sender", {}).get("id")
                        message = messaging_event.get("message", {})
                        message_text = message.get("text", "")
                        message_id = message.get("mid", "")
                        
                        if message_text and message_id:
                            # Deduplicate
                            existing = await db.execute(select(Message).filter(Message.message_id == message_id))
                            if existing.scalar_one_or_none():
                                continue
                                
                            # Upsert conversation
                            conv_res = await db.execute(
                                select(Conversation).filter(
                                    Conversation.store_id == store_id,
                                    Conversation.platform == platform,
                                    Conversation.sender_id == sender_id
                                )
                            )
                            conv = conv_res.scalar_one_or_none()
                            if not conv:
                                conv = Conversation(store_id=store_id, platform=platform, sender_id=sender_id)
                                db.add(conv)
                                await db.commit()
                                await db.refresh(conv)
                                
                            # Save message
                            msg = Message(conversation_id=conv.id, message_id=message_id, text=message_text, sender_type="user")
                            db.add(msg)
                            await db.commit()
                            
                            # Process with AI
                            response = await message_processor.process_message(
                                platform=platform,
                                store_id=str(store_id),
                                sender_id=sender_id,
                                message_text=message_text,
                                db=db
                            )
                            
                            # Reply
                            url = f"https://graph.facebook.com/v18.0/me/messages"
                            payload = {
                                "recipient": {"id": sender_id},
                                "message": {"text": response}
                            }
                            params = {"access_token": access_token}
                            async with httpx.AsyncClient() as client:
                                await client.post(url, json=payload, params=params)
                                
            elif object_type == "whatsapp_business_account":
                for entry in data.get("entry", []):
                    waba_id = entry.get("id")
                    
                    for change in entry.get("changes", []):
                        value = change.get("value", {})
                        phone_number_id = value.get("metadata", {}).get("phone_number_id")
                        
                        if not phone_number_id:
                            continue
                            
                        # Lookup by phone_number_id (and waba_id)
                        result = await db.execute(
                            select(ConnectedWhatsapp).filter(
                                ConnectedWhatsapp.phone_number_id == phone_number_id
                            )
                        )
                        wa = result.scalar_one_or_none()
                        
                        if not wa:
                            logger.error(f"WhatsApp account {phone_number_id} not found in DB")
                            continue
                            
                        store_id = wa.store_id
                        access_token = wa.token
                        
                        if not access_token:
                            # Fallback to system env token if not in DB
                            access_token = getattr(settings, "META_APP_TOKEN", None)
                            
                        if not access_token:
                            logger.error("No access token for WhatsApp")
                            continue
                            
                        for message in value.get("messages", []):
                            sender = message.get("from")
                            message_text = message.get("text", {}).get("body", "")
                            message_id = message.get("id", "")
                            
                            if message_text and message_id:
                                # Deduplicate
                                existing = await db.execute(select(Message).filter(Message.message_id == message_id))
                                if existing.scalar_one_or_none():
                                    continue
                                
                                # Upsert conversation
                                conv_res = await db.execute(
                                    select(Conversation).filter(
                                        Conversation.store_id == store_id,
                                        Conversation.platform == "whatsapp",
                                        Conversation.sender_id == sender
                                    )
                                )
                                conv = conv_res.scalar_one_or_none()
                                if not conv:
                                    conv = Conversation(store_id=store_id, platform="whatsapp", sender_id=sender)
                                    db.add(conv)
                                    await db.commit()
                                    await db.refresh(conv)
                                    
                                # Save message
                                msg = Message(conversation_id=conv.id, message_id=message_id, text=message_text, sender_type="user")
                                db.add(msg)
                                await db.commit()
                                
                                # Process with AI
                                response = await message_processor.process_message(
                                    platform="whatsapp",
                                    store_id=str(store_id),
                                    sender_id=sender,
                                    message_text=message_text,
                                    db=db
                                )
                                
                                # Reply via WhatsApp API
                                url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
                                payload = {
                                    "messaging_product": "whatsapp",
                                    "to": sender,
                                    "text": {"body": response}
                                }
                                headers = {
                                    "Authorization": f"Bearer {access_token}",
                                    "Content-Type": "application/json"
                                }
                                async with httpx.AsyncClient() as client:
                                    await client.post(url, json=payload, headers=headers)
                                    
        except Exception as e:
            logger.error(f"Error processing Meta webhook task: {str(e)}")


@router.post("/telegram/{store_id}")
async def telegram_webhook(
    store_id: UUID,
    request: Request,
    background_tasks: BackgroundTasks
):
    """Handle incoming Telegram messages."""
    data = await request.json()
    background_tasks.add_task(process_telegram_webhook, store_id, data)
    return {"status": "ok"}


async def process_telegram_webhook(store_id: UUID, data: dict):
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Telegram).filter(
                    Telegram.store_id == store_id,
                    Telegram.status == ServiceStatus.ACTIVE
                )
            )
            telegram = result.scalar_one_or_none()
            
            if not telegram:
                return
            
            if "message" in data:
                message = data["message"]
                chat_id = message.get("chat", {}).get("id")
                message_text = message.get("text", "")
                message_id = str(message.get("message_id", ""))
                
                if message_text and message_id:
                    # Deduplicate
                    existing = await db.execute(select(Message).filter(Message.message_id == message_id))
                    if existing.scalar_one_or_none():
                        return
                        
                    # Upsert conversation
                    conv_res = await db.execute(
                        select(Conversation).filter(
                            Conversation.store_id == store_id,
                            Conversation.platform == "telegram",
                            Conversation.sender_id == str(chat_id)
                        )
                    )
                    conv = conv_res.scalar_one_or_none()
                    if not conv:
                        conv = Conversation(store_id=store_id, platform="telegram", sender_id=str(chat_id))
                        db.add(conv)
                        await db.commit()
                        await db.refresh(conv)
                        
                    msg = Message(conversation_id=conv.id, message_id=message_id, text=message_text, sender_type="user")
                    db.add(msg)
                    await db.commit()
                    
                    # Process with AI
                    response = await message_processor.process_message(
                        platform="telegram",
                        store_id=str(store_id),
                        sender_id=str(chat_id),
                        message_text=message_text,
                        db=db
                    )
                    
                    # Send response
                    url = f"https://api.telegram.org/bot{telegram.bot_token}/sendMessage"
                    payload = {
                        "chat_id": chat_id,
                        "text": response
                    }
                    async with httpx.AsyncClient() as client:
                        await client.post(url, json=payload)
                        
        except Exception as e:
            logger.error(f"Error processing Telegram webhook: {str(e)}")

