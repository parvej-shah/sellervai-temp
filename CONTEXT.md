# Project Context — Bizzz Backend

This file summarizes the backend flow, where Chroma is used, and how RAG is implemented so other conversations and contributors can pick up context quickly.

## High-level flow
- Incoming requests:
  - API chat requests: handled by `POST /api/chat` and `POST /api/chat/stream` in app/routes/chat.py
  - Platform messages: handled by webhooks in app/routes/webhooks.py (Messenger, WhatsApp, Telegram, Instagram)
- Routes validate user or platform config and obtain an `AsyncSession` from the DB dependency (`app/lib/database.py`).
- Messages are processed by `app/services/message_processor.py` which calls the AI layer (`app/ai/service.py`).
- The AI layer uses Google Gemini via LangChain (`ChatGoogleGenerativeAI`) and optionally LangChain tools.

## RAG (Retrieval-Augmented Generation)
- Implemented in `app/lib/rag.py` via the `RAGManager` class.
- Embeddings: created with FastEmbed `TextEmbedding` using `intfloat/multilingual-e5-small`.
- What is embedded:
  - `Business.description`
  - Each entry in `Business.products_items` (product name, description, price)
  - Documents are created as `langchain.docstore.document.Document` objects.

## Vector store (Chroma)
- Persistent path: `./chroma_db/{business_id}` (see `RAGManager.persist_directory`).
- Collection name: `biz_{business_id}` (underscores used).
- Write flow: `RAGManager.index_business_data(...)` calls `vector_store.add_documents(documents)` then `vector_store.persist()`.
- Read flow: `RAGManager.query(text, k)` calls `vector_store.similarity_search(text, k)` and returns the `page_content` as context.
- The repository includes a persisted SQLite under `chroma_db/` (e.g. `chroma.sqlite3`).

## Where indexing happens
- Manual/seed indexing: `scripts/seed.py` calls `get_rag_manager(...).index_business_data(..., force=True)` after creating sample data.
- There is no automatic re-index on product/description updates in the webhook/setup flows—updates must call indexing explicitly or be added later (recommended improvement).

## How chat uses RAG
- `AIService.chat_stream()` pre-fetches RAG context for the user message and appends it to the prompt as `[Knowledge Base Context]`.
- For count queries ("how many"), the service also invokes `DatabaseTools.count_products()` and appends `[Live Database Status]` to the prompt.
- The agent exposes the RAG query as a LangChain `Tool` named `knowledge_base_search`, but the streaming path currently uses pre-inserted context rather than a full tool execution loop.

## Data split
- PostgreSQL: users, businesses, configuration, webhooks, platform tokens (encrypted)
- ChromaDB: vectorized business description & product entries for semantic retrieval

## Important notes / Recommendations
- Add indexed update triggers (on product/description changes) or a background job to keep Chroma in sync.
- Consider storing metadata IDs with vectors so replies can include product references/citations.
- If you want true tool-driven streaming (agent runs tools live and streams results), implement a structured agent loop that can call tools and stream intermediate outputs.

---

File generated for quick context in conversations and developer onboarding.
