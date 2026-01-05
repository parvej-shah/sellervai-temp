import os
# Disable ChromaDB telemetry globally
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from chromadb.config import Settings as ChromaSettings
from app.lib.config import settings

# Initialize Google Cloud Embeddings (Lightweight)
embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.GEMINI_EMBEDDING_MODEL,
    google_api_key=settings.GEMINI_API_KEY
)

class RAGManager:
    """Manages Vector Storage and Retrieval for Business-specific data."""
    
    def __init__(self, business_id: str):
        self.business_id = business_id
        self.persist_directory = f"./chroma_db/{business_id}"
        
        # Initialize Vector Store
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
            collection_name=f"biz_{business_id.replace('-', '_')}",
            client_settings=ChromaSettings(anonymized_telemetry=False)
        )

    async def is_indexed(self) -> bool:
        """Check if the vector store already has data."""
        try:
            return self.vector_store._collection.count() > 0
        except Exception:
            return False

    async def index_business_data(self, description: str, products: List[dict], force: bool = False):
        """Index business description and products into the vector store."""
        if not force and await self.is_indexed():
            # Already indexed, skip to avoid API quota issues
            return

        documents = []
        
        # Add business description
        if description:
            documents.append(Document(
                page_content=f"Business Description: {description}",
                metadata={"source": "description", "business_id": self.business_id}
            ))
            
        # Add products
        for product in products:
            content = f"Product: {product.get('name')} | Details: {product.get('description')} | Price: ${product.get('price')}"
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "product", 
                    "product_id": str(product.get('id', '')),
                    "product_name": product.get('name', ''),
                    "business_id": self.business_id
                }
            ))
            
        if documents:
            # Clear existing data for this business and re-index
            # In a production app, you might want to update selectively
            self.vector_store.add_documents(documents)
            self.vector_store.persist()

    async def query(self, text: str, k: int = 3) -> str:
        """Perform semantic search for relevant context."""
        results = self.vector_store.similarity_search(text, k=k)
        if not results:
            return ""
            
        context = "\n".join([res.page_content for res in results])
        return f"Relevant Information found in Knowledge Base:\n{context}"

# Helper to get manager instance
def get_rag_manager(business_id: str) -> RAGManager:
    return RAGManager(business_id)
