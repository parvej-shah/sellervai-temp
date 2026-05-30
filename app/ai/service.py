import logging
from typing import List, Dict, Any, AsyncGenerator, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.lib.config import settings
from app.models.models import Store
from app.lib.rag import get_rag_manager

logger = logging.getLogger(__name__)


class DatabaseTools:
    """Tools for the AI agent to interact with the database."""
    
    def __init__(self, db: AsyncSession, store_id: str):
        self.db = db
        self.store_id = store_id
    
    async def count_products(self, query: str = "") -> str:
        """Count the number of products for a store. Useful for 'How many products do you have?'"""
        logger.debug(f"Counting products for store: {self.store_id}")
        try:
            result = await self.db.execute(
                select(Store).filter(Store.id == self.store_id)
            )
            store = result.scalar_one_or_none()
            if not store:
                return "Store not found."
            count = len(store.products_items or [])
            return f"The store has exactly {count} product(s) in its catalog."
        except Exception as e:
            return f"Error: {str(e)}"

    async def get_store_info(self, query: str = "") -> str:
        """Get general store info. Useful for 'What is this store about?'"""
        logger.debug(f"Getting store info for: {self.store_id}")
        try:
            result = await self.db.execute(
                select(Store).filter(Store.id == self.store_id)
            )
            store = result.scalar_one_or_none()
            if not store:
                return "Store not found."
            return f"Store Name: {store.name}\nDescription: {store.description or 'N/A'}"
        except Exception as e:
            return f"Error: {str(e)}"


def _build_system_prompt(store: Optional[Store] = None) -> str:
    """Build the system prompt with store personalization."""
    base = "You are a helpful store assistant."
    
    if not store:
        return base
    
    parts = []
    
    # Use custom personality prompt if provided
    if store.personality_prompt:
        parts.append(store.personality_prompt)
    else:
        parts.append(f"You are a helpful assistant for the store '{store.name}'.")
    
    if store.description:
        parts.append(f"Store description: {store.description}")
    
    if store.tone:
        parts.append(f"Respond in a {store.tone} tone.")
    
    if store.language and store.language.lower() != "english":
        parts.append(f"Respond primarily in {store.language}.")
    
    if store.welcome_message:
        parts.append(f"When greeting new users, use: {store.welcome_message}")
    
    parts.append("Use the provided context to answer questions accurately. If you don't have specific information, say so honestly.")
    
    return "\n".join(parts)


class AIService:
    """AI service using DeepSeek via OpenAI-compatible API with LangGraph orchestration."""
    
    def __init__(self):
        logger.info(f"Initializing AIService with DeepSeek model: {settings.DEEPSEEK_MODEL}")
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=0,
            streaming=True,
        )
    
    async def _get_store(self, db: AsyncSession, store_id: str) -> Optional[Store]:
        """Fetch store from DB for personalization."""
        try:
            result = await db.execute(
                select(Store).filter(Store.id == store_id)
            )
            return result.scalar_one_or_none()
        except Exception:
            return None

    async def chat_stream(
        self,
        message: str,
        store_id: str,
        db: AsyncSession,
        chat_history: List[Dict[str, str]] = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses using DeepSeek + RAG context with LangGraph orchestration."""
        
        # Fetch store for personalization
        store = await self._get_store(db, store_id)
        
        # Pull RAG context
        rag_manager = get_rag_manager(store_id)
        semantic_context = await rag_manager.query(message)
        
        # Build enhanced message with context
        context_msg = f"\n[Knowledge Base Context]: {semantic_context}" if semantic_context else ""
        full_message = f"{message}{context_msg}"
        
        # Build conversation history
        messages = []
        
        # System prompt with store personalization
        system_prompt = _build_system_prompt(store)
        messages.append(SystemMessage(content=system_prompt))
        
        # Chat history
        if chat_history:
            for m in chat_history:
                if m["role"] == "user":
                    messages.append(HumanMessage(content=m["content"]))
                else:
                    messages.append(AIMessage(content=m["content"]))

        # Check for specific "count" keywords to trigger DB tool manually
        if any(kw in message.lower() for kw in ["how many", "count", "total"]):
            db_tools = DatabaseTools(db, store_id)
            count_info = await db_tools.count_products()
            full_message += f"\n[Live Database Status]: {count_info}"

        messages.append(HumanMessage(content=full_message))

        # Stream using DeepSeek LLM
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
    
    async def chat(
        self,
        message: str,
        store_id: str,
        db: AsyncSession,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """Non-streaming chat using the same logic."""
        response = ""
        async for chunk in self.chat_stream(message, store_id, db, chat_history):
            response += chunk
        return response


# Global AI service instance
ai_service = AIService()
