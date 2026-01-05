from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.lib.database import get_db
from app.models.models import User, Business
from app.schemas.schemas import BusinessCreate, BusinessUpdate, BusinessResponse
from app.lib.auth import get_current_user

router = APIRouter(prefix="/api/business", tags=["Business"])


@router.get("/", response_model=List[BusinessResponse])
async def list_businesses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all businesses for the current user."""
    result = await db.execute(
        select(Business).filter(Business.user_id == current_user.id)
    )
    businesses = result.scalars().all()
    return businesses


@router.post("/", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def create_business(
    business_data: BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new business."""
    new_business = Business(
        user_id=current_user.id,
        name=business_data.name,
        description=business_data.description,
        products_items=business_data.products_items
    )
    
    db.add(new_business)
    await db.commit()
    await db.refresh(new_business)
    
    return new_business


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    return business


@router.put("/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: UUID,
    business_data: BusinessUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Update fields
    if business_data.name is not None:
        business.name = business_data.name
    if business_data.description is not None:
        business.description = business_data.description
    if business_data.products_items is not None:
        business.products_items = business_data.products_items
    
    await db.commit()
    await db.refresh(business)
    
    return business


@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(
    business_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a business."""
    result = await db.execute(
        select(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        )
    )
    business = result.scalar_one_or_none()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    await db.delete(business)
    await db.commit()
    
    return None
