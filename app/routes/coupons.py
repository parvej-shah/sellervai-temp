from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.lib.database import get_db
from app.models.models import User, Store, Coupon
from app.schemas.schemas import CouponCreate, CouponUpdate, CouponResponse
from app.lib.auth import get_current_user

router = APIRouter(prefix="/api/store/{store_id}/coupons", tags=["Coupons"])


async def _get_store_or_404(store_id: UUID, user: User, db: AsyncSession) -> Store:
    result = await db.execute(
        select(Store).where(Store.id == store_id, Store.user_id == user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store


@router.get("/", response_model=List[CouponResponse])
async def list_coupons(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Coupon).where(Coupon.store_id == store_id).order_by(Coupon.code)
    )
    return result.scalars().all()


@router.post("/", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    store_id: UUID,
    data: CouponCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)

    existing = await db.execute(
        select(Coupon).where(Coupon.store_id == store_id, Coupon.code == data.code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Coupon code '{data.code}' already exists in this store",
        )

    coupon = Coupon(store_id=store_id, **data.model_dump())
    db.add(coupon)
    await db.commit()
    await db.refresh(coupon)
    return coupon


@router.get("/{coupon_id}", response_model=CouponResponse)
async def get_coupon(
    store_id: UUID,
    coupon_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Coupon).where(Coupon.id == coupon_id, Coupon.store_id == store_id)
    )
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    return coupon


@router.put("/{coupon_id}", response_model=CouponResponse)
async def update_coupon(
    store_id: UUID,
    coupon_id: UUID,
    data: CouponUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Coupon).where(Coupon.id == coupon_id, Coupon.store_id == store_id)
    )
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(coupon, field, value)

    await db.commit()
    await db.refresh(coupon)
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coupon(
    store_id: UUID,
    coupon_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Coupon).where(Coupon.id == coupon_id, Coupon.store_id == store_id)
    )
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    await db.delete(coupon)
    await db.commit()
