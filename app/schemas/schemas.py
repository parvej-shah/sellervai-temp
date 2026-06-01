from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, UUID4
from app.models.models import ServiceStatus, WebhookStatus, DocumentStatus


# User Schemas
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


# Store Schemas
class StoreBase(BaseModel):
    name: str
    description: Optional[str] = None
    products_items: List[dict] = []
    tone: Optional[str] = None
    personality_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    language: Optional[str] = "english"


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    products_items: Optional[List[dict]] = None
    tone: Optional[str] = None
    personality_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    language: Optional[str] = None


class StoreResponse(StoreBase):
    id: UUID4
    user_id: UUID4
    verification_token: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Store Document Schemas
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


# Service Base Schemas
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


# Messenger Schemas
class MessengerCreate(BaseModel):
    api_key: str
    page_id: Optional[str] = None


class MessengerResponse(ServiceResponse):
    page_id: Optional[str] = None
    
    class Config:
        from_attributes = True


# WhatsApp Schemas
class WhatsAppCreate(BaseModel):
    api_key: str
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None


class WhatsAppResponse(ServiceResponse):
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None
    
    class Config:
        from_attributes = True


# Telegram Schemas
class TelegramCreate(BaseModel):
    bot_token: str
    bot_username: Optional[str] = None


class TelegramResponse(ServiceResponse):
    bot_username: Optional[str] = None
    
    class Config:
        from_attributes = True


# Instagram Schemas
class InstagramCreate(BaseModel):
    api_key: str
    instagram_account_id: Optional[str] = None


class InstagramResponse(ServiceResponse):
    instagram_account_id: Optional[str] = None
    
    class Config:
        from_attributes = True


# Facebook Pages Schemas
class FacebookPagesCreate(BaseModel):
    api_key: str
    page_id: Optional[str] = None


class FacebookPagesResponse(ServiceResponse):
    page_id: Optional[str] = None
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Chat Schemas
class ChatMessage(BaseModel):
    message: str
    store_id: UUID4


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime


# Webhook Verification
class WebhookVerification(BaseModel):
    verified: bool
    message: str
