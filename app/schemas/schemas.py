from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, UUID4

from app.models.models import (
    ServiceStatus, WebhookStatus, DocumentStatus,
    OrderStatus, ResponseLanguage,
)


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class StoreBase(BaseModel):
    name: str
    description: Optional[str] = None
    tone: Optional[str] = None
    personality_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    language: Optional[ResponseLanguage] = ResponseLanguage.ADAPTIVE
    orders_enabled: Optional[bool] = True


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tone: Optional[str] = None
    personality_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    language: Optional[ResponseLanguage] = None
    orders_enabled: Optional[bool] = None


class StoreResponse(StoreBase):
    id: UUID4
    user_id: UUID4
    verification_token: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Store Document
# ---------------------------------------------------------------------------

class StoreDocumentResponse(BaseModel):
    id: UUID4
    store_id: UUID4
    filename: str
    file_type: str
    file_size: Optional[int] = None
    status: DocumentStatus
    chunk_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class ProductBase(BaseModel):
    product_code: str
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    available_count: int = 0
    price: Decimal
    discount: Optional[Decimal] = None
    enabled: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    available_count: Optional[int] = None
    price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    enabled: Optional[bool] = None


class ProductResponse(ProductBase):
    id: UUID4
    store_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Coupon
# ---------------------------------------------------------------------------

class CouponBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_amount: Optional[Decimal] = None
    discount_percent: Optional[Decimal] = None
    min_order_amount: Optional[Decimal] = None
    max_uses: Optional[int] = None
    expires_at: Optional[datetime] = None
    enabled: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    description: Optional[str] = None
    discount_amount: Optional[Decimal] = None
    discount_percent: Optional[Decimal] = None
    min_order_amount: Optional[Decimal] = None
    max_uses: Optional[int] = None
    expires_at: Optional[datetime] = None
    enabled: Optional[bool] = None


class CouponResponse(CouponBase):
    id: UUID4
    store_id: UUID4
    used_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_phone_2: Optional[str] = None
    delivery_address: str
    product_code: str
    quantity: int = 1
    coupon_code: Optional[str] = None
    extra_info: Optional[Dict[str, Any]] = {}


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_phone_2: Optional[str] = None
    delivery_address: Optional[str] = None
    extra_info: Optional[Dict[str, Any]] = None


class OrderResponse(BaseModel):
    id: UUID4
    store_id: UUID4
    order_number: str
    customer_name: str
    customer_phone: str
    customer_phone_2: Optional[str] = None
    delivery_address: str
    product_code: str
    product_name: str
    product_price: Decimal
    quantity: int
    coupon_code: Optional[str] = None
    discount_applied: Decimal
    total_amount: Decimal
    extra_info: Dict[str, Any]
    status: OrderStatus
    platform: Optional[str] = None
    sender_id: Optional[str] = None
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------------------------

class ConversationMemoryResponse(BaseModel):
    id: UUID4
    conversation_id: UUID4
    memory: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Platform service schemas
# ---------------------------------------------------------------------------

class ServiceBase(BaseModel):
    webhook_status: WebhookStatus = WebhookStatus.PENDING
    status: ServiceStatus = ServiceStatus.INACTIVE


class ServiceResponse(ServiceBase):
    id: UUID4
    store_id: UUID4
    added_date: datetime
    webhook_added_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessengerCreate(BaseModel):
    api_key: str
    page_id: Optional[str] = None


class MessengerResponse(ServiceResponse):
    page_id: Optional[str] = None

    class Config:
        from_attributes = True


class WhatsAppCreate(BaseModel):
    api_key: str
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None


class WhatsAppResponse(ServiceResponse):
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None

    class Config:
        from_attributes = True


class TelegramCreate(BaseModel):
    bot_token: str
    bot_username: Optional[str] = None


class TelegramResponse(ServiceResponse):
    bot_username: Optional[str] = None

    class Config:
        from_attributes = True


class InstagramCreate(BaseModel):
    api_key: str
    instagram_account_id: Optional[str] = None


class InstagramResponse(ServiceResponse):
    instagram_account_id: Optional[str] = None

    class Config:
        from_attributes = True


class FacebookPagesCreate(BaseModel):
    api_key: str
    page_id: Optional[str] = None


class FacebookPagesResponse(ServiceResponse):
    page_id: Optional[str] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    message: str
    store_id: UUID4


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

class WebhookVerification(BaseModel):
    verified: bool
    message: str
