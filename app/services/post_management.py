"""
Post management service for handling posts, comments, and autopilot logic.
"""

import logging
import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.models import PagePost, PostComment, Store, ConnectedPage, ConnectedInstagram
from app.ai.service import AIService

logger = logging.getLogger(__name__)


class PostManagementService:
    """Service for managing social media posts and automating responses."""

    def __init__(self):
        self.ai_service = AIService()

    async def extract_post_image_text(self, post_id: str, page_token: str) -> tuple:
        """
        Extract image URL and text from a post using Vision API.
        Returns: (image_url, image_text)
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get post details from Graph API
                url = f"https://graph.facebook.com/v25.0/{post_id}"
                params = {
                    "fields": "full_picture,message,picture",
                    "access_token": page_token
                }
                response = await client.get(url, params=params)
                data = response.json()

                if "error" in data:
                    logger.error(f"Error fetching post {post_id}: {data['error']}")
                    return None, None

                image_url = data.get("full_picture") or data.get("picture")

                if not image_url:
                    return None, None

                # Extract text from image using vision
                image_text = await self._extract_text_from_image_url(image_url)
                return image_url, image_text

        except Exception as e:
            logger.error(f"Error extracting image text from post {post_id}: {str(e)}")
            return None, None

    async def _extract_text_from_image_url(self, image_url: str) -> str:
        """
        Extract text from image URL using AI vision capabilities.
        """
        try:
            # Use the existing AI service to analyze the image
            # This would typically use GPT-4 Vision or similar
            # For now, we'll use a placeholder that integrates with your AI service
            response = await self.ai_service.analyze_image(image_url)
            return response.get("text", "") if response else ""
        except Exception as e:
            logger.error(f"Error extracting text from image {image_url}: {str(e)}")
            return ""

    async def generate_initial_knowledge(self, post_text: str, image_text: str) -> str:
        """
        Generate initial knowledge/context for a post from its content.
        """
        try:
            combined_text = f"{post_text}\n\n{image_text}" if image_text else post_text

            prompt = f"""Based on this social media post, generate a concise knowledge base entry that would help an AI assistant respond to customer comments about this post.

Post content:
{combined_text}

Generate a brief, clear knowledge summary (2-3 sentences) that captures:
- What the post is about
- Key details customers should know (products, prices, availability, etc.)
- Action items or next steps

Keep it friendly and factual."""

            response = await self.ai_service.generate_text(prompt)
            return response.strip() if response else ""

        except Exception as e:
            logger.error(f"Error generating initial knowledge: {str(e)}")
            return ""

    async def save_new_post(
        self,
        db: AsyncSession,
        store_id: UUID,
        page_id: str,
        post_id: str,
        message: str,
        image_url: str = None,
        image_text: str = None,
        knowledge: str = None,
    ) -> PagePost:
        """
        Save a new post to the database.
        """
        try:
            # Check if post already exists
            result = await db.execute(
                select(PagePost).filter(PagePost.post_id == post_id)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing

            post = PagePost(
                store_id=store_id,
                page_id=page_id,
                post_id=post_id,
                message=message,
                image_url=image_url,
                image_text=image_text,
                knowledge=knowledge,
                knowledge_updated=knowledge is not None,
                autopilot_paused=False,
            )
            db.add(post)
            await db.commit()
            await db.refresh(post)
            logger.info(f"Saved new post {post_id} for store {store_id}")
            return post

        except Exception as e:
            logger.error(f"Error saving post {post_id}: {str(e)}")
            raise

    async def should_reply_to_comment(self, db: AsyncSession, store_id: UUID, post_id: str) -> bool:
        """
        Determine if the bot should reply to comments on this post.
        Returns True if:
        - Store has autopilot enabled
        - Post is not paused
        """
        try:
            # Get store autopilot setting
            store_result = await db.execute(
                select(Store).filter(Store.id == store_id)
            )
            store = store_result.scalar_one_or_none()
            if not store or not store.autopilot_enabled:
                return False

            # Get post pause status
            post_result = await db.execute(
                select(PagePost).filter(PagePost.post_id == post_id)
            )
            post = post_result.scalar_one_or_none()
            if not post or post.autopilot_paused:
                return False

            return True

        except Exception as e:
            logger.error(f"Error checking if should reply: {str(e)}")
            return False

    async def generate_comment_reply(
        self,
        comment_text: str,
        post_knowledge: str,
        store_context: dict,
    ) -> str:
        """
        Generate an AI response to a comment using post knowledge and store context.
        """
        try:
            personality = store_context.get("personality_prompt", "Be helpful and friendly.")
            tone = store_context.get("tone", "friendly")

            prompt = f"""You are a customer service assistant for a business.

Personality: {personality}
Tone: {tone}

Post context/knowledge:
{post_knowledge}

Customer comment:
{comment_text}

Generate a brief, friendly response to the customer's comment. Keep it concise (1-2 sentences) and helpful."""

            response = await self.ai_service.generate_text(prompt)
            return response.strip() if response else ""

        except Exception as e:
            logger.error(f"Error generating comment reply: {str(e)}")
            return ""

    async def save_comment_and_reply(
        self,
        db: AsyncSession,
        post_id: str,
        store_id: UUID,
        comment_id: str,
        sender_id: str,
        sender_name: str,
        text: str,
        reply_text: str = None,
    ) -> PostComment:
        """
        Save a comment and its reply to the database.
        """
        try:
            # Check if comment already exists
            result = await db.execute(
                select(PostComment).filter(PostComment.comment_id == comment_id)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing

            comment = PostComment(
                post_id=post_id,
                store_id=store_id,
                comment_id=comment_id,
                sender_id=sender_id,
                sender_name=sender_name,
                text=text,
                replied=reply_text is not None,
                reply_text=reply_text,
            )
            db.add(comment)
            await db.commit()
            await db.refresh(comment)
            logger.info(f"Saved comment {comment_id} on post {post_id}")
            return comment

        except Exception as e:
            logger.error(f"Error saving comment {comment_id}: {str(e)}")
            raise

    async def post_comment_reply(
        self,
        comment_id: str,
        reply_text: str,
        page_token: str,
    ) -> bool:
        """
        Reply to a comment via Meta Graph API.
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://graph.facebook.com/v25.0/{comment_id}/private_replies"
                payload = {
                    "message": reply_text,
                    "access_token": page_token,
                }
                response = await client.post(url, data=payload)
                
                if response.status_code in (200, 201):
                    logger.info(f"Posted reply to comment {comment_id}")
                    return True
                else:
                    logger.error(f"Error posting reply: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            logger.error(f"Error posting comment reply: {str(e)}")
            return False

    async def get_page_token(
        self,
        db: AsyncSession,
        page_id: str,
    ) -> str:
        """
        Get the access token for a specific page.
        """
        try:
            result = await db.execute(
                select(ConnectedPage).filter(ConnectedPage.page_id == page_id)
            )
            page = result.scalar_one_or_none()
            return page.token if page else None

        except Exception as e:
            logger.error(f"Error getting page token: {str(e)}")
            return None

    async def get_ig_token(
        self,
        db: AsyncSession,
        ig_user_id: str,
    ) -> str:
        """
        Get the access token for a specific Instagram account.
        """
        try:
            result = await db.execute(
                select(ConnectedInstagram).filter(ConnectedInstagram.ig_user_id == ig_user_id)
            )
            ig = result.scalar_one_or_none()
            return ig.token if ig else None

        except Exception as e:
            logger.error(f"Error getting IG token: {str(e)}")
            return None


# Global instance
post_management_service = PostManagementService()
