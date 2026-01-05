import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.lib.database import Base


class ServiceStatus(str, enum.Enum):
    PAUSED = "paused"
    ACTIVE = "active"
    INACTIVE = "inactive"


class WebhookStatus(str, enum.Enum):
    VERIFIED = "verified"
    PENDING = "pending"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    businesses = relationship("Business", back_populates="user", cascade="all, delete-orphan")


class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    products_items = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="businesses")
    messenger = relationship("Messenger", back_populates="business", uselist=False, cascade="all, delete-orphan")
    whatsapp = relationship("WhatsApp", back_populates="business", uselist=False, cascade="all, delete-orphan")
    telegram = relationship("Telegram", back_populates="business", uselist=False, cascade="all, delete-orphan")
    instagram = relationship("Instagram", back_populates="business", uselist=False, cascade="all, delete-orphan")
    facebook_pages = relationship("FacebookPages", back_populates="business", uselist=False, cascade="all, delete-orphan")


class Messenger(Base):
    __tablename__ = "messenger"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    page_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="messenger")


class WhatsApp(Base):
    __tablename__ = "whatsapp"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    phone_number_id = Column(String(255), nullable=True)
    business_account_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="whatsapp")


class Telegram(Base):
    __tablename__ = "telegram"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True)
    bot_token = Column(String(500), nullable=False)  # Encrypted bot token
    bot_username = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="telegram")


class Instagram(Base):
    __tablename__ = "instagram"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    instagram_account_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="instagram")


class FacebookPages(Base):
    __tablename__ = "facebook_pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    page_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="facebook_pages")
