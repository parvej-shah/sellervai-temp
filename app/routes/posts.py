"""
Post management API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel

from app.lib.database import get_db
from app.lib.auth import get_current_user
from app.models.models import User, Store, PagePost, PostComment, ConnectedPage, ConnectedInstagram, PostType
from app.services.post_generation import post_generation_service


# Request models
class AutopilotToggleRequest(BaseModel):
    enabled: bool

class UpdateKnowledgeRequest(BaseModel):
    knowledge: str

class BulkPostActionRequest(BaseModel):
    store_id: UUID
    post_ids: List[str]

class GenerateProductPostRequest(BaseModel):
    product_id: UUID

class GenerateContentPostRequest(BaseModel):
    category: str  # "meme" or "quote"

class PublishPostRequest(BaseModel):
    post_text: str
    post_type: str  # "product", "meme", "quote"
    product_id: Optional[UUID] = None
    platforms: List[str]  # ["facebook", "instagram"] etc
    page_ids: Optional[List[str]] = None  # Facebook page IDs
    ig_user_ids: Optional[List[str]] = None  # Instagram user IDs


router = APIRouter(prefix="/api/posts", tags=["Posts"])


# ============================================================================
# Autopilot Management
# ============================================================================

@router.get("/autopilot/{store_id}")
async def get_autopilot_status(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get autopilot status for a store."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    return {
        "store_id": str(store_id),
        "autopilot_enabled": store.autopilot_enabled,
    }


@router.post("/autopilot/{store_id}/toggle")
async def toggle_autopilot(
    store_id: UUID,
    payload: AutopilotToggleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggle autopilot mode for a store."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    enabled = payload.enabled
    store.autopilot_enabled = enabled
    await db.commit()

    return {
        "store_id": str(store_id),
        "autopilot_enabled": enabled,
    }


# ============================================================================
# Post Management
# ============================================================================

@router.get("/store/{store_id}")
async def get_store_posts(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all posts for a store."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    posts_result = await db.execute(
        select(PagePost)
            .filter(PagePost.store_id == store_id)
            .options(selectinload(PagePost.comments))
    )
    posts = posts_result.scalars().all()

    return {
        "store_id": str(store_id),
        "autopilot_enabled": store.autopilot_enabled,
        "posts": [
            {
                "id": str(post.id),
                "post_id": post.post_id,
                "page_id": post.page_id,
                "message": post.message,
                "image_url": post.image_url,
                "knowledge": post.knowledge,
                "knowledge_updated": post.knowledge_updated,
                "autopilot_paused": post.autopilot_paused,
                "created_at": post.created_at.isoformat(),
                "comment_count": len(post.comments) if post.comments else 0,
            }
            for post in posts
        ],
    }


@router.post("/post/{post_id}/knowledge")
async def update_post_knowledge(
    post_id: str,
    payload: UpdateKnowledgeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update knowledge for a specific post."""
    result = await db.execute(select(PagePost).filter(PagePost.post_id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Verify ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == post.store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    knowledge = payload.knowledge
    post.knowledge = knowledge
    post.knowledge_updated = True
    await db.commit()

    return {
        "post_id": post_id,
        "knowledge": post.knowledge,
        "knowledge_updated": True,
    }


@router.post("/post/{post_id}/pause")
async def pause_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Pause autopilot for a specific post."""
    result = await db.execute(select(PagePost).filter(PagePost.post_id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Verify ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == post.store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    post.autopilot_paused = True
    await db.commit()

    return {
        "post_id": post_id,
        "autopilot_paused": True,
    }


@router.post("/post/{post_id}/resume")
async def resume_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Resume autopilot for a specific post."""
    result = await db.execute(select(PagePost).filter(PagePost.post_id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Verify ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == post.store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    post.autopilot_paused = False
    await db.commit()

    return {
        "post_id": post_id,
        "autopilot_paused": False,
    }


@router.post("/posts/bulk-pause")
async def bulk_pause_posts(
    payload: BulkPostActionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Pause multiple posts at once."""
    store_id = payload.store_id
    post_ids = payload.post_ids

    # Verify store ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    if not post_ids:
        return {"paused_count": 0}

    # Update all posts
    await db.execute(
        update(PagePost)
        .where(
            (PagePost.post_id.in_(post_ids))
            & (PagePost.store_id == store_id)
        )
        .values(autopilot_paused=True)
    )
    await db.commit()

    return {
        "paused_count": len(post_ids),
    }


@router.post("/posts/bulk-resume")
async def bulk_resume_posts(
    payload: BulkPostActionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Resume multiple posts at once."""
    store_id = payload.store_id
    post_ids = payload.post_ids

    # Verify store ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    if not post_ids:
        return {"resumed_count": 0}

    # Update all posts
    await db.execute(
        update(PagePost)
        .where(
            (PagePost.post_id.in_(post_ids))
            & (PagePost.store_id == store_id)
        )
        .values(autopilot_paused=False)
    )
    await db.commit()

    return {
        "resumed_count": len(post_ids),
    }


# ============================================================================
# Post Comments
# ============================================================================

@router.get("/post/{post_id}/comments")
async def get_post_comments(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all comments on a post."""
    # Get the post first
    post_result = await db.execute(
        select(PagePost).filter(PagePost.post_id == post_id)
    )
    post = post_result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Verify ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == post.store_id, Store.user_id == current_user.id)
    )
    if not store_result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Get comments
    comments_result = await db.execute(
        select(PostComment).filter(PostComment.post_id == post_id)
    )
    comments = comments_result.scalars().all()

    return {
        "post_id": post_id,
        "comments": [
            {
                "id": str(comment.id),
                "comment_id": comment.comment_id,
                "sender_id": comment.sender_id,
                "sender_name": comment.sender_name,
                "text": comment.text,
                "replied": comment.replied,
                "reply_text": comment.reply_text,
                "created_at": comment.created_at.isoformat(),
            }
            for comment in comments
        ],
    }


# ============================================================================
# Post Generation
# ============================================================================

@router.post("/generate/product")
async def generate_product_post(
    store_id: UUID,
    payload: GenerateProductPostRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a post for a product."""
    # Verify store ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = store_result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Generate post text
    post_text = await post_generation_service.generate_product_post(
        payload.product_id, store, db
    )

    if not post_text:
        raise HTTPException(status_code=500, detail="Failed to generate post")

    return {
        "post_text": post_text,
        "post_type": "product",
        "product_id": str(payload.product_id),
    }


@router.post("/generate/content")
async def generate_content_post(
    store_id: UUID,
    payload: GenerateContentPostRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a content post (meme, quote, etc.)."""
    # Verify store ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = store_result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Validate category
    if payload.category not in ["meme", "quote"]:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Generate post text
    post_text = await post_generation_service.generate_content_post(
        payload.category, store
    )

    if not post_text:
        raise HTTPException(status_code=500, detail="Failed to generate post")

    return {
        "post_text": post_text,
        "post_type": payload.category,
    }


@router.post("/publish/{store_id}")
async def publish_post(
    store_id: UUID,
    payload: PublishPostRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate post and publish to selected platforms."""
    # Verify store ownership
    store_result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = store_result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    published_posts = []

    # Publish to Facebook
    if "facebook" in payload.platforms and payload.page_ids:
        for page_id in payload.page_ids:
            # Get page token
            page_result = await db.execute(
                select(ConnectedPage).filter(ConnectedPage.page_id == page_id)
            )
            page = page_result.scalar_one_or_none()
            if not page:
                continue

            # Publish
            post_id = await post_generation_service.publish_to_facebook(
                page_id, payload.post_text, page.token
            )
            
            print("Post Type: ", payload.post_type, PostType(payload.post_type.upper()))


            if post_id:
                # Save to database
                db_post = await post_generation_service.save_generated_post(
                    db,
                    store_id=store_id,
                    page_id=page_id,
                    post_id=post_id,
                    post_text=payload.post_text,
                    platform="facebook",
                    post_type=PostType(payload.post_type.upper()),
                    product_id=payload.product_id,
                )
                published_posts.append({
                    "platform": "facebook",
                    "page_id": page_id,
                    "post_id": post_id,
                })

    # Publish to Instagram
    if "instagram" in payload.platforms and payload.ig_user_ids:
        for ig_user_id in payload.ig_user_ids:
            # Get IG token
            ig_result = await db.execute(
                select(ConnectedInstagram).filter(ConnectedInstagram.ig_user_id == ig_user_id)
            )
            ig = ig_result.scalar_one_or_none()
            if not ig:
                continue

            # Publish
            post_id = await post_generation_service.publish_to_instagram(
                ig_user_id, payload.post_text, ig.token
            )

            if post_id:
                # Save to database
                db_post = await post_generation_service.save_generated_post(
                    db,
                    store_id=store_id,
                    page_id=ig_user_id,
                    post_id=post_id,
                    post_text=payload.post_text,
                    platform="instagram",
                    post_type=PostType(payload.post_type.upper()),
                    product_id=payload.product_id,
                )
                published_posts.append({
                    "platform": "instagram",
                    "ig_user_id": ig_user_id,
                    "post_id": post_id,
                })

    if not published_posts:
        raise HTTPException(status_code=500, detail="Failed to publish to any platform")

    return {
        "status": "success",
        "published_posts": published_posts,
    }

