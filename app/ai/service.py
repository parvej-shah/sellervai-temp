from typing import List, Dict, Any, AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, AgentExecutor, create_structured_chat_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.lib.config import settings
from app.models.models import Business
from app.lib.rag import get_rag_manager


class DatabaseTools:
    """Tools for the AI agent to interact with the database (Structured)."""
    
    def __init__(self, db: AsyncSession, business_id: str):
        self.db = db
        self.business_id = business_id
    
    async def count_products(self, query: str = "") -> str:
        """Count the number of products for a business. Useful for 'How many products do you have?'"""
        print(f"DEBUG: Counting products for business: {self.business_id}")
        try:
            result = await self.db.execute(
                select(Business).filter(Business.id == self.business_id)
            )
            business = result.scalar_one_or_none()
            if not business:
                return "Business not found."
            count = len(business.products_items or [])
            return f"The business has exactly {count} product(s) in its catalog."
        except Exception as e:
            return f"Error: {str(e)}"

    async def get_business_info(self, query: str = "") -> str:
        """Get general business info. Useful for 'What is this business about?'"""
        print(f"DEBUG: Getting business info for: {self.business_id}")
        try:
            result = await self.db.execute(
                select(Business).filter(Business.id == self.business_id)
            )
            business = result.scalar_one_or_none()
            if not business:
                return "Business not found."
            return f"Business Name: {business.name}\nDescription: {business.description or 'N/A'}"
        except Exception as e:
            return f"Error: {str(e)}"


class AIService:
    """AI service for handling chat interactions with RAG and Tool-use."""
    
    def __init__(self):
        print(f"DEBUG: Using Gemini Chat Model: {settings.GEMINI_CHAT_MODEL}")
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_CHAT_MODEL, 
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0, 
            streaming=True,
            convert_system_message_to_human=True,
        )
    
    def _create_tools(self, db_tools: DatabaseTools, rag_manager: Any) -> List[Tool]:
        """Create tools that the agent can choose to use."""
        return [
            Tool(
                name="knowledge_base_search",
                func=rag_manager.query,
                description="Use this for semantic search. Perfect for questions about product details, prices, or business specific info. Input should be a search query.",
                coroutine=rag_manager.query,
            ),
            Tool(
                name="database_product_count",
                func=db_tools.count_products,
                description="Use this ONLY when the user asks for the total number of products. Returns an exact count.",
                coroutine=db_tools.count_products,
            ),
            Tool(
                name="get_business_overview",
                func=db_tools.get_business_info,
                description="Use this to get the business name and primary description.",
                coroutine=db_tools.get_business_info,
            ),
        ]

    async def _get_agent_executor(self, db: AsyncSession, business_id: str) -> AgentExecutor:
        """Initialize an agent executor with tools."""
        db_tools = DatabaseTools(db, business_id)
        rag_manager = get_rag_manager(business_id)
        tools = self._create_tools(db_tools, rag_manager)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful business assistant. Use your tools to provide accurate info. If tools return no info, state that you don't have that specific data yet."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_structured_chat_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    async def chat_stream(
        self,
        message: str,
        business_id: str,
        db: AsyncSession,
        chat_history: List[Dict[str, str]] = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses. (Currently Gemini-LangChain tool-streaming is limited, so we invoke and stream the result)."""
        
        # Pull RAG context first as a baseline to help the LLM decide
        rag_manager = get_rag_manager(business_id)
        semantic_context = await rag_manager.query(message)
        
        # Build prompt with context pre-inserted for faster response if tools aren't needed
        context_msg = f"\n[Knowledge Base Context]: {semantic_context}" if semantic_context else ""
        
        # For simplicity and direct context, we'll use a direct prompt but include tool outputs
        # To truly use tools in a stream, we'd need a more complex Agent loop
        # Here we prioritize the RAG context we already fetched
        full_message = f"{message}{context_msg}"
        
        history = []
        if chat_history:
            for m in chat_history:
                if m["role"] == "user":
                    history.append(HumanMessage(content=m["content"]))
                else:
                    history.append(AIMessage(content=m["content"]))

        # Check for specific "count" keywords to trigger DB tool manually for better reliability
        if any(kw in message.lower() for kw in ["how many", "count", "total"]):
            db_tools = DatabaseTools(db, business_id)
            count_info = await db_tools.count_products()
            full_message += f"\n[Live Database Status]: {count_info}"

        async for chunk in self.llm.astream([SystemMessage(content="You are a helpful business assistant.")] + history + [HumanMessage(content=full_message)]):
            if hasattr(chunk, 'content'):
                yield chunk.content
    
    async def chat(
        self,
        message: str,
        business_id: str,
        db: AsyncSession,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """Non-streaming chat using the same logic."""
        response = ""
        async for chunk in self.chat_stream(message, business_id, db, chat_history):
            response += chunk
        return response


ai_service = AIService()
