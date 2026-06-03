import secrets
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
    verification_token = Column(String(255), unique=True, index=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    
    # Personalization / LLM Characterization
    tone = Column(String(100), nullable=True)  # e.g., "friendly", "professional", "casual"
    personality_prompt = Column(Text, nullable=True)  # Custom system prompt for LLM behavior
    welcome_message = Column(Text, nullable=True)  # Greeting message for new conversations
    language = Column(String(50), default="english", nullable=True)  # Preferred response language
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="stores")
    facebook_page = relationship("ConnectedPage", back_populates="store", uselist=False, cascade="all, delete-orphan")
    whatsapp = relationship("ConnectedWhatsapp", back_populates="store", uselist=False, cascade="all, delete-orphan")
    telegram = relationship("Telegram", back_populates="store", uselist=False, cascade="all, delete-orphan")
    instagram = relationship("ConnectedInstagram", back_populates="store", uselist=False, cascade="all, delete-orphan")
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


class ConnectedPage(Base):
    __tablename__ = "connected_pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    page_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=False)  # Page token
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="facebook_page")
    user = relationship("User")


class ConnectedWhatsapp(Base):
    __tablename__ = "connected_whatsapp"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    waba_id = Column(String(255), nullable=False)
    phone_number_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=True) # WhatsApp API token
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


class ConnectedInstagram(Base):
    __tablename__ = "connected_instagram"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    ig_user_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=True) # IG Page Token
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="instagram")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False) # e.g., "messenger", "instagram", "whatsapp", "telegram"
    sender_id = Column(String(255), nullable=False) # The customer's ID on that platform
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    store = relationship("Store")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(String(255), nullable=False, unique=True) # Deduplication from Meta
    text = Column(Text, nullable=True)
    sender_type = Column(String(50), nullable=False) # "user", "bot", "agent"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    conversation = relationship("Conversation", back_populates="messages")
# Add token to models
