import secrets
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


def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)


@router.get("/", response_model=List[StoreResponse])
async def list_stores(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Store).where(Store.user_id == current_user.id))
    return result.scalars().all()


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_store = Store(
        user_id=current_user.id,
        name=store_data.name,
        description=store_data.description,
        tone=store_data.tone,
        personality_prompt=store_data.personality_prompt,
        welcome_message=store_data.welcome_message,
        language=store_data.language,
        orders_enabled=store_data.orders_enabled if store_data.orders_enabled is not None else True,
        verification_token=generate_verification_token(),
    )
    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)
    return new_store


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Store).where(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: UUID,
    store_data: StoreUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Store).where(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    update_fields = store_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(store, field, value)

    if not store.verification_token:
        store.verification_token = generate_verification_token()

    await db.commit()
    await db.refresh(store)
    return store


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Store).where(Store.id == store_id, Store.user_id == current_user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    await db.delete(store)
    await db.commit()
