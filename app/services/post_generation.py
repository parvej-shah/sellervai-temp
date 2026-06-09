"""
Post generation service for creating and publishing social media posts.
"""

import logging
import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.models import Store, Product, PagePost, ConnectedPage, ConnectedInstagram, PostType, PostSource
from app.ai.service import AIService

logger = logging.getLogger(__name__)


class PostGenerationService:
    """Service for generating and publishing social media posts."""

    def __init__(self):
        self.ai_service = AIService()

    async def generate_product_post(
        self,
        product_id: UUID,
        store: Store,
        db: AsyncSession,
    ) -> str:
        """
        Generate a social media post for a product.
        """
        try:
            # Get product details
            result = await db.execute(
                select(Product).filter(Product.id == product_id, Product.store_id == store.id)
            )
            product = result.scalar_one_or_none()
            if not product:
                logger.error(f"Product {product_id} not found")
                return ""

            prompt = f"""Generate an engaging social media post for this product:

Product Name: {product.name}
Description: {product.description or '(No description)'}
Price: ${product.price}
{'Discount: $' + str(product.discount) if product.discount else ''}

Store Context:
- Tone: {store.tone or 'friendly'}
- Personality: {store.personality_prompt or 'professional'}

Create a concise, engaging post (1-3 sentences) suitable for Facebook and Instagram that:
- Highlights the product benefits
- Creates urgency or interest
- Uses emojis naturally
- Ends with a call-to-action (DM to order, etc.)

Just provide the post text, no explanations."""

            post_text = await self.ai_service.generate_text(prompt)
            return post_text.strip() if post_text else ""

        except Exception as e:
            logger.error(f"Error generating product post: {str(e)}")
            return ""

    async def generate_content_post(
        self,
        post_category: str,  # "meme" or "quote"
        store: Store,
    ) -> str:
        """
        Generate a non-product post (meme, quote, etc.).
        """
        try:
            category_instructions = {
                "meme": "Create a funny, relatable meme caption that would appeal to the store's customers.",
                "quote": "Create an inspiring or motivational quote that aligns with the store's values.",
            }

            instructions = category_instructions.get(
                post_category,
                "Create an engaging social media post."
            )

            prompt = f"""Generate a {post_category} for a social media post.

{instructions}

Store Context:
- Name: {store.name}
- Description: {store.description or '(No description)'}
- Tone: {store.tone or 'friendly'}
- Personality: {store.personality_prompt or 'professional'}

Requirements:
- Make it engaging and shareable
- Use emojis naturally
- Keep it concise (1-3 sentences max)
- Make it relevant to the store's industry/products

Just provide the post text, no explanations."""

            post_text = await self.ai_service.generate_text(prompt)
            return post_text.strip() if post_text else ""

        except Exception as e:
            logger.error(f"Error generating content post: {str(e)}")
            return ""

    async def publish_to_facebook(
        self,
        page_id: str,
        post_text: str,
        page_token: str,
    ) -> str:
        """
        Publish a post to Facebook.
        Returns the post_id if successful, empty string on failure.
        """
        try:
            timeout = httpx.Timeout(
                connect=10.0,
                read=60.0,
                write=60.0,
                pool=60.0,
            )
            async with httpx.AsyncClient(timeout=timeout) as client:
                url = f"https://graph.facebook.com/v25.0/{page_id}/feed"
                payload = {
                    "message": post_text,
                    "access_token": page_token,
                }
                response = await client.post(url, data=payload)

                if response.status_code in (200, 201):
                    data = response.json()
                    post_id = data.get("id")
                    logger.info(f"Published to Facebook: {post_id}")
                    return post_id
                else:
                    logger.error(f"Facebook API error: {response.status_code} - {response.text}")
                    return ""

        except Exception as e:
            logger.error(f"Error publishing to Facebook: {repr(e)}", exc_info=True)
            return ""

    async def publish_to_instagram(
        self,
        ig_user_id: str,
        post_text: str,
        ig_token: str,
    ) -> str:
        """
        Publish a post to Instagram.
        Note: Instagram API for carousel/image posts is more complex.
        For text-only posts, we use comments/captions.
        Returns the post_id if successful, empty string on failure.
        """
        try:
            timeout = httpx.Timeout(
                connect=10.0,
                read=60.0,
                write=60.0,
                pool=60.0,
            )
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Instagram requires media creation first, which is complex
                # For now, we'll use the media endpoint with a text container
                # In production, you'd generate an image with the text

                url = f"https://graph.instagram.com/v25.0/{ig_user_id}/media"
                payload = {
                    "media_type": "CAROUSEL",
                    "caption": post_text,
                    "access_token": ig_token,
                }

                response = await client.post(url, data=payload)

                if response.status_code in (200, 201):
                    data = response.json()
                    media_id = data.get("id")
                    logger.info(f"Published to Instagram: {media_id}")
                    return media_id
                else:
                    logger.error(f"Instagram API error: {response.status_code} - {response.text}")
                    return ""

        except Exception as e:
            logger.error(f"Error publishing to Instagram: {str(e)}")
            return ""

    async def save_generated_post(
        self,
        db: AsyncSession,
        store_id: UUID,
        page_id: str,
        post_id: str,
        post_text: str,
        platform: str,
        post_type: PostType,
        product_id: UUID = None,
    ) -> PagePost:
        """
        Save a generated post to the database.
        """
        try:
            post = PagePost(
                store_id=store_id,
                page_id=page_id,
                post_id=post_id,
                platform=platform,
                post_type=post_type,
                post_source=PostSource.GENERATED,
                message=post_text,
                product_id=product_id,
                knowledge=post_text,  # Use generated text as initial knowledge
                knowledge_updated=True,
                autopilot_paused=False,
            )
            db.add(post)
            await db.commit()
            await db.refresh(post)
            logger.info(f"Saved generated post {post_id}")
            return post

        except Exception as e:
            logger.error(f"Error saving generated post: {str(e)}")
            raise


# Global instance
post_generation_service = PostGenerationService()
