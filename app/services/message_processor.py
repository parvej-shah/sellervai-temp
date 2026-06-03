import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.models import Conversation, Message
from app.ai.service import ai_service

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Central service that processes inbound messages from all platforms."""

    async def _get_or_create_conversation(
        self,
        db: AsyncSession,
        store_id: str,
        platform: str,
        sender_id: str,
    ) -> Conversation:
        result = await db.execute(
            select(Conversation).where(
                Conversation.store_id == store_id,
                Conversation.platform == platform,
                Conversation.sender_id == sender_id,
            )
        )
        conv = result.scalar_one_or_none()
        if not conv:
            conv = Conversation(
                store_id=store_id,
                platform=platform,
                sender_id=sender_id,
            )
            db.add(conv)
            await db.flush()  # get the id without full commit
        return conv

    async def _save_message(
        self,
        db: AsyncSession,
        conversation_id: str,
        message_id: str,
        text: str,
        sender_type: str,  # "user" | "bot"
    ) -> None:
        """Persist a message; skip if already stored (deduplication)."""
        result = await db.execute(
            select(Message).where(Message.message_id == message_id)
        )
        if result.scalar_one_or_none():
            return
        msg = Message(
            conversation_id=conversation_id,
            message_id=message_id,
            text=text,
            sender_type=sender_type,
        )
        db.add(msg)

    async def process_message(
        self,
        platform: str,
        store_id: str,
        sender_id: str,
        message_text: str,
        db: AsyncSession,
        message_id: Optional[str] = None,
    ) -> str:
        """
        Process an inbound customer message:
        1. Get/create conversation record.
        2. Save the inbound message.
        3. Generate AI response with full context (history + memory + tools).
        4. Save the bot response.
        5. Return the response text.
        """
        try:
            logger.info(f"Processing {platform} message from {sender_id} for store {store_id}")

            # Conversation record
            conv = await self._get_or_create_conversation(db, store_id, platform, sender_id)

            # Save inbound message
            dedup_id = message_id or f"{platform}-{sender_id}-{message_text[:32]}"
            await self._save_message(db, str(conv.id), dedup_id, message_text, "user")
            await db.flush()

            # Generate response (history is fetched inside ai_service via conversation_id)
            response = await ai_service.chat(
                message=message_text,
                store_id=store_id,
                db=db,
                conversation_id=str(conv.id),
                sender_id=sender_id,
                platform=platform,
            )

            # Save bot response
            bot_msg_id = f"bot-{dedup_id}"
            await self._save_message(db, str(conv.id), bot_msg_id, response, "bot")
            await db.commit()

            logger.info(f"Response for {platform}/{sender_id}: {response[:80]}...")
            return response

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await db.rollback()
            return "I'm sorry, I encountered an issue. Please try again."

    async def process_comment(
        self,
        platform: str,
        store_id: str,
        post_id: str,
        commenter_id: str,
        comment_text: str,
        db: AsyncSession,
    ) -> str:
        """Process a comment (no persistent conversation, simple AI reply)."""
        try:
            logger.info(f"Processing {platform} comment from {commenter_id} for store {store_id}")
            response = await ai_service.chat(
                message=comment_text,
                store_id=store_id,
                db=db,
                sender_id=commenter_id,
                platform=platform,
            )
            return response
        except Exception as e:
            logger.error(f"Error processing comment: {e}", exc_info=True)
            return "Thank you for your comment!"


# Global instance
message_processor = MessageProcessor()
