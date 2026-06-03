import secrets
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Text, JSON,
    Integer, Boolean, Numeric, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.lib.database import Base


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

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


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class ResponseLanguage(str, enum.Enum):
    ADAPTIVE = "adaptive"
    BANGLA = "bangla"
    ENGLISH = "english"


# ---------------------------------------------------------------------------
# Core user / auth
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    stores = relationship("Store", back_populates="user", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class Store(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    verification_token = Column(
        String(255), unique=True, index=True, nullable=False,
        default=lambda: secrets.token_urlsafe(32)
    )

    # AI / persona
    tone = Column(String(100), nullable=True)
    personality_prompt = Column(Text, nullable=True)
    welcome_message = Column(Text, nullable=True)
    language = Column(
        SQLEnum(ResponseLanguage),
        default=ResponseLanguage.ADAPTIVE,
        nullable=False
    )

    # Order config
    orders_enabled = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="stores")
    facebook_page = relationship("ConnectedPage", back_populates="store", uselist=False, cascade="all, delete-orphan")
    whatsapp = relationship("ConnectedWhatsapp", back_populates="store", uselist=False, cascade="all, delete-orphan")
    telegram = relationship("Telegram", back_populates="store", uselist=False, cascade="all, delete-orphan")
    instagram = relationship("ConnectedInstagram", back_populates="store", uselist=False, cascade="all, delete-orphan")
    documents = relationship("StoreDocument", back_populates="store", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="store", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="store", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="store", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)

    product_code = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)      # URL or file path
    available_count = Column(Integer, default=0, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), nullable=True)  # absolute discount amount
    enabled = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="products")


# ---------------------------------------------------------------------------
# Coupon
# ---------------------------------------------------------------------------

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)

    code = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    discount_amount = Column(Numeric(10, 2), nullable=True)   # fixed discount
    discount_percent = Column(Numeric(5, 2), nullable=True)   # percentage discount
    min_order_amount = Column(Numeric(10, 2), nullable=True)  # minimum order value
    max_uses = Column(Integer, nullable=True)                 # None = unlimited
    used_count = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="coupons")


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)

    # Order identification
    order_number = Column(String(50), unique=True, nullable=False,
                          default=lambda: f"ORD-{secrets.token_hex(4).upper()}")

    # Customer info (collected via chatbot)
    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_phone_2 = Column(String(20), nullable=True)
    delivery_address = Column(Text, nullable=False)

    # Product (single product per order - product_code is fixed at order time)
    product_code = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    # Discount / coupon
    coupon_code = Column(String(100), nullable=True)
    discount_applied = Column(Numeric(10, 2), default=0, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Additional info checklist (flexible extra fields)
    extra_info = Column(JSON, default=dict, nullable=False)

    # Status
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    # Platform context (which conversation created this order)
    platform = Column(String(50), nullable=True)
    sender_id = Column(String(255), nullable=True)  # platform user ID
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="orders")


# ---------------------------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------------------------

class ConversationMemory(Base):
    """Stores extracted user facts (name, phone, etc.) per conversation."""
    __tablename__ = "conversation_memory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"),
                             nullable=False, unique=True)
    # Structured memory – key/value pairs extracted from chat
    memory = Column(JSON, default=dict, nullable=False)
    # e.g. {"name": "Rahim", "phone": "017XXXXXXXX", "address": "Dhaka"}
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="memory")


# ---------------------------------------------------------------------------
# Platform connections
# ---------------------------------------------------------------------------

class StoreDocument(Base):
    """Tracks files uploaded to a store for RAG indexing."""
    __tablename__ = "store_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=True)
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.PROCESSING, nullable=False)
    chunk_count = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="documents")


class ConnectedPage(Base):
    __tablename__ = "connected_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    page_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="facebook_page")
    user = relationship("User")


class ConnectedWhatsapp(Base):
    __tablename__ = "connected_whatsapp"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    waba_id = Column(String(255), nullable=False)
    phone_number_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="whatsapp")


class Telegram(Base):
    __tablename__ = "telegram"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    bot_token = Column(String(500), nullable=False)
    bot_username = Column(String(255), nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    webhook_added_date = Column(DateTime, nullable=True)
    webhook_status = Column(SQLEnum(WebhookStatus), default=WebhookStatus.PENDING, nullable=False)
    status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.INACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="telegram")


class ConnectedInstagram(Base):
    __tablename__ = "connected_instagram"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, unique=True)
    ig_user_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="instagram")


# ---------------------------------------------------------------------------
# Conversation / messages
# ---------------------------------------------------------------------------

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    sender_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    memory = relationship("ConversationMemory", back_populates="conversation", uselist=False,
                          cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(String(255), nullable=False, unique=True)
    text = Column(Text, nullable=True)
    sender_type = Column(String(50), nullable=False)  # "user" | "bot" | "agent"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
