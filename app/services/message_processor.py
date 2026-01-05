from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Business
from app.ai.service import ai_service
import logging

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Central service for processing messages from all platforms."""
    
    async def process_message(
        self,
        platform: str,
        business_id: str,
        sender_id: str,
        message_text: str,
        db: AsyncSession
    ) -> str:
        """
        Process incoming message and generate AI response.
        """
        try:
            logger.info(f"Processing message from {platform} for business {business_id}")
            
            # Generate AI response
            response = await ai_service.chat(
                message=message_text,
                business_id=business_id,
                db=db
            )
            
            logger.info(f"Generated response for {platform}: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    async def process_comment(
        self,
        platform: str,
        business_id: str,
        post_id: str,
        commenter_id: str,
        comment_text: str,
        db: AsyncSession
    ) -> str:
        """
        Process incoming comment and generate AI response.
        """
        try:
            logger.info(f"Processing comment from {platform} for business {business_id}")
            
            # Generate AI response
            response = await ai_service.chat(
                message=comment_text,
                business_id=business_id,
                db=db
            )
            
            logger.info(f"Generated comment response for {platform}: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error processing comment: {str(e)}")
            return "Thank you for your comment!"


# Global message processor instance
message_processor = MessageProcessor()
