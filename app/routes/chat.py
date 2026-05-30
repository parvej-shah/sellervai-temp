from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Dict

from app.lib.database import get_db
from app.models.models import User, Store
from app.schemas.schemas import ChatMessage
from app.lib.auth import get_current_user
from app.ai.service import ai_service
from sqlalchemy import select

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/stream")
async def stream_chat(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Stream chat responses from the AI."""
    
    # Verify store belongs to user
    result = await db.execute(
        select(Store).filter(
            Store.id == chat_data.store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found or access denied"
        )
    
    async def generate():
        async for chunk in ai_service.chat_stream(
            message=chat_data.message,
            store_id=str(chat_data.store_id),
            db=db
        ):
            yield chunk
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/")
async def chat(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a complete chat response (non-streaming)."""
    
    # Verify store belongs to user
    result = await db.execute(
        select(Store).filter(
            Store.id == chat_data.store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found or access denied"
        )
    
    response = await ai_service.chat(
        message=chat_data.message,
        store_id=str(chat_data.store_id),
        db=db
    )
    
    return {"response": response}
