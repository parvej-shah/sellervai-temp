from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.lib.database import get_db
from app.models.models import User, Store
from app.schemas.schemas import StoreCreate, StoreUpdate, StoreResponse
from app.lib.auth import get_current_user

router = APIRouter(prefix="/api/store", tags=["Store"])


@router.get("/", response_model=List[StoreResponse])
async def list_stores(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all stores for the current user."""
    result = await db.execute(
        select(Store).filter(Store.user_id == current_user.id)
    )
    stores = result.scalars().all()
    return stores


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new store."""
    new_store = Store(
        user_id=current_user.id,
        name=store_data.name,
        description=store_data.description,
        products_items=store_data.products_items,
        tone=store_data.tone,
        personality_prompt=store_data.personality_prompt,
        welcome_message=store_data.welcome_message,
        language=store_data.language,
    )
    
    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)
    
    return new_store


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific store."""
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    return store


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: UUID,
    store_data: StoreUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a store."""
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    # Update fields
    if store_data.name is not None:
        store.name = store_data.name
    if store_data.description is not None:
        store.description = store_data.description
    if store_data.products_items is not None:
        store.products_items = store_data.products_items
    if store_data.tone is not None:
        store.tone = store_data.tone
    if store_data.personality_prompt is not None:
        store.personality_prompt = store_data.personality_prompt
    if store_data.welcome_message is not None:
        store.welcome_message = store_data.welcome_message
    if store_data.language is not None:
        store.language = store_data.language
    
    await db.commit()
    await db.refresh(store)
    
    return store


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a store."""
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    await db.delete(store)
    await db.commit()
    
    return None
