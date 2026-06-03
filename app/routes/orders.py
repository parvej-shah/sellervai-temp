import secrets
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from uuid import UUID

from app.lib.database import get_db
from app.models.models import User, Store, Product, Coupon, Order, OrderStatus
from app.schemas.schemas import OrderCreate, OrderUpdate, OrderResponse
from app.lib.auth import get_current_user

router = APIRouter(prefix="/api/store/{store_id}/orders", tags=["Orders"])


async def _get_store_or_404(store_id: UUID, user: User, db: AsyncSession) -> Store:
    result = await db.execute(
        select(Store).where(Store.id == store_id, Store.user_id == user.id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    store_id: UUID,
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all orders for a store, optionally filtered by status."""
    await _get_store_or_404(store_id, current_user, db)
    query = select(Order).where(Order.store_id == store_id).order_by(desc(Order.created_at))
    if status_filter:
        query = query.where(Order.status == status_filter)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    store_id: UUID,
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually create an order (dashboard use)."""
    store = await _get_store_or_404(store_id, current_user, db)

    if not store.orders_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This store does not accept orders.",
        )

    # Fetch product
    result = await db.execute(
        select(Product).where(
            Product.store_id == store_id,
            Product.product_code == data.product_code,
            Product.enabled == True,
        )
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{data.product_code}' not found or unavailable.",
        )
    if product.available_count < data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.available_count} unit(s) in stock.",
        )

    unit_price = Decimal(str(product.price))
    if product.discount:
        unit_price -= Decimal(str(product.discount))
    subtotal = unit_price * data.quantity

    # Coupon
    discount_applied = Decimal("0")
    validated_coupon = None
    if data.coupon_code:
        result2 = await db.execute(
            select(Coupon).where(
                Coupon.store_id == store_id,
                Coupon.code == data.coupon_code,
                Coupon.enabled == True,
            )
        )
        coupon = result2.scalar_one_or_none()
        if coupon:
            if coupon.discount_percent:
                discount_applied = subtotal * coupon.discount_percent / 100
            elif coupon.discount_amount:
                discount_applied = min(coupon.discount_amount, subtotal)
            validated_coupon = coupon

    total = subtotal - discount_applied

    order = Order(
        store_id=store_id,
        order_number=f"ORD-{secrets.token_hex(4).upper()}",
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        customer_phone_2=data.customer_phone_2,
        delivery_address=data.delivery_address,
        product_code=product.product_code,
        product_name=product.name,
        product_price=unit_price,
        quantity=data.quantity,
        coupon_code=data.coupon_code if validated_coupon else None,
        discount_applied=discount_applied,
        total_amount=total,
        extra_info=data.extra_info or {},
        status=OrderStatus.PENDING,
    )
    db.add(order)
    product.available_count -= data.quantity
    if validated_coupon:
        validated_coupon.used_count += 1

    await db.commit()
    await db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    store_id: UUID,
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.store_id == store_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    store_id: UUID,
    order_id: UUID,
    data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update order status or customer details."""
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.store_id == store_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    await db.commit()
    await db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    store_id: UUID,
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_store_or_404(store_id, current_user, db)
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.store_id == store_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    await db.delete(order)
    await db.commit()
