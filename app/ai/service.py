import json
import logging
import secrets
from decimal import Decimal
from typing import List, Dict, Any, AsyncGenerator, Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.config import settings
from app.models.models import (
    Store, Product, Coupon, Order, Conversation, Message,
    ConversationMemory, OrderStatus, ResponseLanguage,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _price(val) -> str:
    """Format a numeric/Decimal price nicely."""
    try:
        return f"{Decimal(str(val)):.2f}"
    except Exception:
        return str(val)


# ---------------------------------------------------------------------------
# Database tool implementations (async functions called by the agent)
# ---------------------------------------------------------------------------

class StoreTools:
    """All database operations the AI agent can perform for a store."""

    def __init__(self, db: AsyncSession, store_id: str, conversation_id: Optional[str] = None):
        self.db = db
        self.store_id = store_id
        self.conversation_id = conversation_id

    # ── Products ────────────────────────────────────────────────────────────

    async def list_products(self) -> str:
        """Return all enabled products for the store."""
        result = await self.db.execute(
            select(Product).where(
                Product.store_id == self.store_id,
                Product.enabled == True,
            ).order_by(Product.name)
        )
        products = result.scalars().all()
        if not products:
            return "No products are currently available."
        lines = ["Available products:"]
        for p in products:
            eff_price = Decimal(str(p.price)) - (Decimal(str(p.discount)) if p.discount else Decimal("0"))
            stock = f"(in stock: {p.available_count})" if p.available_count > 0 else "(out of stock)"
            disc = f", Discount: -{_price(p.discount)}" if p.discount else ""
            lines.append(
                f"- [{p.product_code}] {p.name} | Price: {_price(p.price)}{disc} | "
                f"Effective: {_price(eff_price)} {stock}"
            )
            if p.description:
                lines.append(f"  Description: {p.description}")
        return "\n".join(lines)

    async def get_product(self, product_code: str) -> str:
        """Get details for a specific product by code."""
        result = await self.db.execute(
            select(Product).where(
                Product.store_id == self.store_id,
                Product.product_code == product_code,
            )
        )
        p = result.scalar_one_or_none()
        if not p:
            return f"Product with code '{product_code}' not found."
        eff = Decimal(str(p.price)) - (Decimal(str(p.discount)) if p.discount else Decimal("0"))
        status = "Available" if p.enabled and p.available_count > 0 else "Unavailable"
        disc = f"\nDiscount: -{_price(p.discount)}" if p.discount else ""
        return (
            f"Product: {p.name}\nCode: {p.product_code}\n"
            f"Price: {_price(p.price)}{disc}\nEffective Price: {_price(eff)}\n"
            f"Stock: {p.available_count}\nStatus: {status}\n"
            f"Description: {p.description or 'N/A'}"
        )

    async def count_products(self) -> str:
        """Count available products."""
        result = await self.db.execute(
            select(Product).where(
                Product.store_id == self.store_id,
                Product.enabled == True,
            )
        )
        count = len(result.scalars().all())
        return f"The store has {count} available product(s)."

    # ── Coupons ─────────────────────────────────────────────────────────────

    async def validate_coupon(self, coupon_code: str, order_amount: float = 0) -> str:
        """Check if a coupon is valid and return discount info."""
        from datetime import datetime
        result = await self.db.execute(
            select(Coupon).where(
                Coupon.store_id == self.store_id,
                Coupon.code == coupon_code,
                Coupon.enabled == True,
            )
        )
        coupon = result.scalar_one_or_none()
        if not coupon:
            return f"Coupon '{coupon_code}' is not valid."
        if coupon.expires_at and coupon.expires_at < datetime.utcnow():
            return f"Coupon '{coupon_code}' has expired."
        if coupon.max_uses and coupon.used_count >= coupon.max_uses:
            return f"Coupon '{coupon_code}' has reached its usage limit."
        if coupon.min_order_amount and Decimal(str(order_amount)) < coupon.min_order_amount:
            return (
                f"Coupon '{coupon_code}' requires a minimum order of {_price(coupon.min_order_amount)}. "
                f"Your current order is {_price(order_amount)}."
            )
        if coupon.discount_percent:
            disc = Decimal(str(order_amount)) * coupon.discount_percent / 100
            return f"Coupon '{coupon_code}' gives {_price(coupon.discount_percent)}% off. Discount: {_price(disc)}"
        if coupon.discount_amount:
            return f"Coupon '{coupon_code}' gives a flat {_price(coupon.discount_amount)} discount."
        return f"Coupon '{coupon_code}' is valid but has no discount configured."

    # ── Orders ───────────────────────────────────────────────────────────────

    async def create_order(
        self,
        customer_name: str,
        customer_phone: str,
        delivery_address: str,
        product_code: str,
        quantity: int = 1,
        customer_phone_2: Optional[str] = None,
        coupon_code: Optional[str] = None,
        extra_info: Optional[Dict[str, Any]] = None,
        platform: Optional[str] = None,
        sender_id: Optional[str] = None,
    ) -> str:
        """Create a new order and return confirmation details."""
        from datetime import datetime

        # Fetch product
        result = await self.db.execute(
            select(Product).where(
                Product.store_id == self.store_id,
                Product.product_code == product_code,
                Product.enabled == True,
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            return f"Cannot create order: product '{product_code}' not found or unavailable."
        if product.available_count < quantity:
            return (
                f"Cannot create order: only {product.available_count} unit(s) of "
                f"'{product.name}' are in stock, but you requested {quantity}."
            )

        unit_price = Decimal(str(product.price))
        if product.discount:
            unit_price -= Decimal(str(product.discount))
        subtotal = unit_price * quantity

        # Apply coupon
        discount_applied = Decimal("0")
        validated_coupon = None
        if coupon_code:
            result2 = await self.db.execute(
                select(Coupon).where(
                    Coupon.store_id == self.store_id,
                    Coupon.code == coupon_code,
                    Coupon.enabled == True,
                )
            )
            coupon = result2.scalar_one_or_none()
            if coupon:
                if coupon.discount_percent:
                    discount_applied = subtotal * coupon.discount_percent / 100
                elif coupon.discount_amount:
                    discount_applied = coupon.discount_amount
                validated_coupon = coupon

        total = subtotal - discount_applied

        order_number = f"ORD-{secrets.token_hex(4).upper()}"
        order = Order(
            store_id=self.store_id,
            order_number=order_number,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_phone_2=customer_phone_2,
            delivery_address=delivery_address,
            product_code=product.product_code,
            product_name=product.name,
            product_price=unit_price,
            quantity=quantity,
            coupon_code=coupon_code if validated_coupon else None,
            discount_applied=discount_applied,
            total_amount=total,
            extra_info=extra_info or {},
            status=OrderStatus.PENDING,
            platform=platform,
            sender_id=sender_id,
            conversation_id=self.conversation_id,
        )
        self.db.add(order)

        # Decrement stock
        product.available_count -= quantity

        # Increment coupon usage
        if validated_coupon:
            validated_coupon.used_count += 1

        await self.db.commit()

        return (
            f"Order created successfully!\n"
            f"Order ID: {order_number}\n"
            f"Product: {product.name} x{quantity}\n"
            f"Unit Price: {_price(unit_price)}\n"
            f"Discount: -{_price(discount_applied)}\n"
            f"Total: {_price(total)}\n"
            f"Delivery to: {delivery_address}\n"
            f"Contact: {customer_phone}\n"
            f"Status: Pending"
        )

    async def lookup_orders(self, sender_id: str, platform: Optional[str] = None) -> str:
        """Look up all orders placed by this conversation's sender."""
        query = select(Order).where(
            Order.store_id == self.store_id,
            Order.sender_id == sender_id,
        ).order_by(desc(Order.created_at)).limit(10)
        result = await self.db.execute(query)
        orders = result.scalars().all()
        if not orders:
            return "No orders found for you."
        lines = [f"Your orders ({len(orders)} found):"]
        for o in orders:
            lines.append(
                f"- {o.order_number} | {o.product_name} x{o.quantity} | "
                f"Total: {_price(o.total_amount)} | Status: {o.status.value} | "
                f"Date: {o.order_date.strftime('%Y-%m-%d %H:%M')}"
            )
        return "\n".join(lines)

    async def count_orders(self, sender_id: str) -> str:
        """Count orders placed by this user."""
        result = await self.db.execute(
            select(Order).where(
                Order.store_id == self.store_id,
                Order.sender_id == sender_id,
            )
        )
        count = len(result.scalars().all())
        return f"You have placed {count} order(s) with this store."

    # ── Memory ───────────────────────────────────────────────────────────────

    async def get_memory(self) -> Dict[str, Any]:
        """Retrieve conversation memory (extracted user info)."""
        if not self.conversation_id:
            return {}
        result = await self.db.execute(
            select(ConversationMemory).where(
                ConversationMemory.conversation_id == self.conversation_id
            )
        )
        mem = result.scalar_one_or_none()
        return mem.memory if mem else {}

    async def update_memory(self, updates: Dict[str, Any]) -> None:
        """Merge new facts into conversation memory."""
        if not self.conversation_id:
            return
        result = await self.db.execute(
            select(ConversationMemory).where(
                ConversationMemory.conversation_id == self.conversation_id
            )
        )
        mem = result.scalar_one_or_none()
        if mem:
            merged = {**mem.memory, **updates}
            mem.memory = merged
        else:
            mem = ConversationMemory(
                conversation_id=self.conversation_id,
                memory=updates,
            )
            self.db.add(mem)
        await self.db.commit()


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------

def _build_system_prompt(store: Store, memory: Dict[str, Any]) -> str:
    """Build a rich system prompt using store config and conversation memory."""

    # Language instruction
    lang = store.language or ResponseLanguage.ADAPTIVE
    if lang == ResponseLanguage.BANGLA:
        lang_instruction = (
            "Always respond in Bangla (Bengali script). Never use Markdown formatting. "
            "Use plain text only."
        )
    elif lang == ResponseLanguage.ENGLISH:
        lang_instruction = (
            "Always respond in English. Never use Markdown formatting. "
            "Use plain text only."
        )
    else:  # adaptive
        lang_instruction = (
            "Detect the language the user is writing in and respond in the same language "
            "(Bangla or English). Never use Markdown formatting. Use plain text only."
        )

    # Core identity
    if store.personality_prompt:
        identity = store.personality_prompt
    else:
        identity = f"You are a helpful assistant for the store '{store.name}'."

    parts = [identity]

    if store.description:
        parts.append(f"Store: {store.description}")

    if store.tone:
        parts.append(f"Tone: Be {store.tone}.")

    parts.append(lang_instruction)

    # Order capability
    if store.orders_enabled:
        parts.append(
            "\nYou can take orders from customers. When a customer wants to order a product:\n"
            "1. Ask for their full name.\n"
            "2. Ask for their primary phone number.\n"
            "3. Ask for their delivery address.\n"
            "4. Ask if they have a second phone number (optional).\n"
            "5. Ask if they have a coupon code (optional).\n"
            "6. Show a complete summary of all collected info and ask for final confirmation.\n"
            "7. Only after the customer confirms, call the create_order tool.\n"
            "8. Tell the customer their order ID and status after creation.\n"
            "Do not create an order without explicit final confirmation from the customer."
        )
    else:
        parts.append("\nThis store does not currently accept orders.")

    # Memory context
    if memory:
        mem_lines = ["Known information about this customer:"]
        for k, v in memory.items():
            mem_lines.append(f"  - {k}: {v}")
        parts.append("\n".join(mem_lines))

    parts.append(
        "\nAvailable tools: list_products, get_product, count_products, "
        "validate_coupon, create_order, lookup_orders, count_orders.\n"
        "Call tools when the customer asks about products, prices, stock, orders, or coupons. "
        "Never fabricate product info or order IDs."
    )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Agentic AI Service
# ---------------------------------------------------------------------------

class AIService:
    """Agentic AI service with database tools, memory, and conversation history."""

    TOOL_TRIGGERS = {
        "list_products": ["products", "what do you sell", "what do you have", "product list", "catalog", "menu"],
        "count_products": ["how many products", "count products", "number of products"],
        "lookup_orders": ["my orders", "order history", "my order", "check order", "order status"],
        "count_orders": ["how many orders", "count orders", "total orders"],
    }

    def __init__(self):
        logger.info(f"Initializing AIService with model: {settings.DEEPSEEK_MODEL}")
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=0.3,
            streaming=True,
        )

    async def _get_store(self, db: AsyncSession, store_id: str) -> Optional[Store]:
        try:
            result = await db.execute(select(Store).where(Store.id == store_id))
            return result.scalar_one_or_none()
        except Exception:
            return None

    async def _get_conversation_history(
        self, db: AsyncSession, conversation_id: str, limit: int = 15
    ) -> List[Dict[str, str]]:
        """Fetch last N messages for context window."""
        try:
            result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(desc(Message.created_at))
                .limit(limit)
            )
            msgs = result.scalars().all()
            # Reverse to chronological order
            return [
                {"role": "user" if m.sender_type == "user" else "assistant", "content": m.text or ""}
                for m in reversed(msgs)
            ]
        except Exception:
            return []

    async def _run_tools(
        self,
        message: str,
        tools: "StoreTools",
        sender_id: Optional[str] = None,
    ) -> str:
        """Detect tool intent and run the appropriate tool, returning injected context."""
        msg_lower = message.lower()
        context_parts = []

        # Product queries
        if any(kw in msg_lower for kw in self.TOOL_TRIGGERS["list_products"]):
            context_parts.append(await tools.list_products())

        elif any(kw in msg_lower for kw in self.TOOL_TRIGGERS["count_products"]):
            context_parts.append(await tools.count_products())

        # Order queries
        if sender_id and any(kw in msg_lower for kw in self.TOOL_TRIGGERS["lookup_orders"]):
            context_parts.append(await tools.lookup_orders(sender_id))

        elif sender_id and any(kw in msg_lower for kw in self.TOOL_TRIGGERS["count_orders"]):
            context_parts.append(await tools.count_orders(sender_id))

        # Coupon validation
        if "coupon" in msg_lower or "discount code" in msg_lower or "promo" in msg_lower:
            # Try to extract coupon code from message (simple heuristic)
            words = message.upper().split()
            for word in words:
                if len(word) >= 4 and word.isalnum():
                    result = await tools.validate_coupon(word)
                    if "not valid" not in result and "not found" not in result.lower():
                        context_parts.append(result)
                        break

        return "\n\n".join(context_parts) if context_parts else ""

    async def _extract_and_save_memory(
        self,
        message: str,
        tools: "StoreTools",
    ) -> None:
        """Simple regex-free heuristic extraction of user facts into memory."""
        import re
        updates: Dict[str, Any] = {}

        # Phone number patterns (BD-style)
        phone_match = re.search(r"(?<!\d)(0[0-9]{10}|[+]880[0-9]{10})(?!\d)", message)
        if phone_match:
            updates["phone"] = phone_match.group()

        # Name hints: "my name is X" / "I am X" / "ami X"
        name_match = re.search(
            r"(?:my name is|i am|i'm|amar naam|ami)\s+([A-Za-z\u0980-\u09FF][A-Za-z\u0980-\u09FF\s]{1,40})",
            message, re.IGNORECASE
        )
        if name_match:
            updates["name"] = name_match.group(1).strip()

        if updates:
            await tools.update_memory(updates)

    async def chat_stream(
        self,
        message: str,
        store_id: str,
        db: AsyncSession,
        conversation_id: Optional[str] = None,
        sender_id: Optional[str] = None,
        platform: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream AI response with tools, memory, and history."""

        store = await self._get_store(db, store_id)
        tools = StoreTools(db, store_id, conversation_id)

        # Fetch DB conversation history if conversation_id given
        if conversation_id and not chat_history:
            chat_history = await self._get_conversation_history(db, conversation_id)

        # Get conversation memory
        memory = await tools.get_memory()

        # Save any extractable facts from this message
        await self._extract_and_save_memory(message, tools)

        # Run database tools for injected context
        tool_context = await self._run_tools(message, tools, sender_id)

        # RAG context
        rag_context = ""
        try:
            from app.lib.rag import get_rag_manager
            rag_manager = get_rag_manager(store_id)
            rag_context = await rag_manager.query(message)
        except ImportError:
            pass
        except Exception:
            pass

        # Build LangChain message list
        messages = []

        system_prompt = _build_system_prompt(store, memory) if store else (
            "You are a helpful store assistant. Do not use Markdown. Reply in plain text only."
        )
        messages.append(SystemMessage(content=system_prompt))

        # Conversation history
        if chat_history:
            for m in chat_history:
                if m["role"] == "user":
                    messages.append(HumanMessage(content=m["content"]))
                else:
                    messages.append(AIMessage(content=m["content"]))

        # Augment the current message
        augments = []
        if rag_context:
            augments.append(f"[Knowledge Base]\n{rag_context}")
        if tool_context:
            augments.append(f"[Live Store Data]\n{tool_context}")
        if memory:
            augments.append(f"[Customer Memory]\n{json.dumps(memory, ensure_ascii=False)}")

        full_message = message
        if augments:
            full_message += "\n\n" + "\n\n".join(augments)

        messages.append(HumanMessage(content=full_message))

        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content

    async def chat(
        self,
        message: str,
        store_id: str,
        db: AsyncSession,
        conversation_id: Optional[str] = None,
        sender_id: Optional[str] = None,
        platform: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Non-streaming chat."""
        response = ""
        async for chunk in self.chat_stream(
            message, 
            store_id, 
            db,
            conversation_id=conversation_id,
            sender_id=sender_id,
            platform=platform,
            chat_history=chat_history,
        ):
            response += chunk
        return response


    async def generate_text(self, prompt: str) -> str:
        """Utility for one-off text generation."""
        try:
            print(f"Generating text with prompt: {prompt}")
            # ainvoke takes a list of messages directly
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            print(f"Generation response: {response}")
            
            # response is an AIMessage object, extract content safely
            if response and hasattr(response, 'content'):
                return response.content
            return ""
        except Exception as e:
            logger.error(f"Error in generate_text: {str(e)}")
            return ""


    async def create_order_from_chat(
        self,
        store_id: str,
        db: AsyncSession,
        conversation_id: Optional[str],
        sender_id: Optional[str],
        platform: Optional[str],
        customer_name: str,
        customer_phone: str,
        delivery_address: str,
        product_code: str,
        quantity: int = 1,
        customer_phone_2: Optional[str] = None,
        coupon_code: Optional[str] = None,
        extra_info: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Direct order creation called by the agentic flow after confirmation."""
        tools = StoreTools(db, store_id, conversation_id)
        return await tools.create_order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            product_code=product_code,
            quantity=quantity,
            customer_phone_2=customer_phone_2,
            coupon_code=coupon_code,
            extra_info=extra_info,
            platform=platform,
            sender_id=sender_id,
        )


# Global singleton
ai_service = AIService()
