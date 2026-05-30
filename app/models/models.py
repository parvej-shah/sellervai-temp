import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.lib.database import Base


class ServiceStatus(str, enum.Enum):
    PAUSED = "PAUSED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class WebhookStatus(str, enum.Enum):
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    FAILED = "FAILED"


class DocumentStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


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
    stores = relationship("Store", back_populates="user", cascade="all, delete-orphan")


class Store(Base):
    __tablename__ = "stores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    products_items = Column(JSON, default=list, nullable=False)
    
    # Personalization / LLM Characterization
    tone = Column(String(100), nullable=True)  # e.g., "friendly", "professional", "casual"
    personality_prompt = Column(Text, nullable=True)  # Custom system prompt for LLM behavior
    welcome_message = Column(Text, nullable=True)  # Greeting message for new conversations
    language = Column(String(50), default="english", nullable=True)  # Preferred response language
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="stores")
    messenger = relationship("Messenger", back_populates="store", uselist=False, cascade="all, delete-orphan")
    whatsapp = relationship("WhatsApp", back_populates="store", uselist=False, cascade="all, delete-orphan")
    telegram = relationship("Telegram", back_populates="store", uselist=False, cascade="all, delete-orphan")
    instagram = relationship("Instagram", back_populates="store", uselist=False, cascade="all, delete-orphan")
    facebook_pages = relationship("FacebookPages", back_populates="store", uselist=False, cascade="all, delete-orphan")
    documents = relationship("StoreDocument", back_populates="store", cascade="all, delete-orphan")


class StoreDocument(Base):
    """Tracks files uploaded to a store for RAG indexing."""
    __tablename__ = "store_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, txt, docx, csv
    file_size = Column(Integer, nullable=True)  # bytes
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.PROCESSING, nullable=False)
    chunk_count = Column(Integer, default=0, nullable=True)  # number of chunks indexed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="documents")


class Messenger(Base):
    __tablename__ = "messenger"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    page_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="messenger")


class WhatsApp(Base):
    __tablename__ = "whatsapp"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
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
    store = relationship("Store", back_populates="whatsapp")


class Telegram(Base):
    __tablename__ = "telegram"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    bot_token = Column(String(500), nullable=False)  # Encrypted bot token
    bot_username = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="telegram")


class Instagram(Base):
    __tablename__ = "instagram"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    instagram_account_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="instagram")


class FacebookPages(Base):
    __tablename__ = "facebook_pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted access token
    page_id = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="facebook_pages")
