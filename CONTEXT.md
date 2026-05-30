# Project Context — Bizzz Backend

This file summarizes the backend flow, current store-centric naming, and how RAG is implemented so other conversations and contributors can pick up context quickly.

## High-level flow
- Incoming requests:
  - API chat requests: handled by `POST /api/chat` and `POST /api/chat/stream` in `app/routes/chat.py`
  - Platform messages: handled by webhooks in `app/routes/webhooks.py` (Messenger, WhatsApp, Telegram, Instagram)
- Routes validate user or platform config and obtain an `AsyncSession` from the DB dependency (`app/lib/database.py`).
- Messages are processed by `app/services/message_processor.py` which calls the AI layer (`app/ai/service.py`).
- The AI layer uses DeepSeek via `ChatOpenAI` and builds prompts with optional RAG context.

## RAG (Retrieval-Augmented Generation)
- Implemented in `app/lib/rag.py` via the `RAGManager` class.
- Embeddings: `langchain_community.embeddings.FastEmbedEmbeddings` with `intfloat/multilingual-e5-small`.
- Vector store: `langchain_community.vectorstores.PGVector`.
- What is embedded:
  - `Store.description`
  - Each entry in `Store.products_items` (product name, description, price)
  - Uploaded documents are created as `langchain_core.documents.Document` objects.

## Vector store (PGVector)
- Backed by PostgreSQL using the app's database URL converted to a sync connection string.
- Collection name: `store_{store_id}`.
- Write flow: `RAGManager.index_store_data(...)` and `RAGManager.index_file(...)` call `vector_store.add_documents(...)`.
- Read flow: `RAGManager.query(text, k)` calls `vector_store.similarity_search(text, k)` and returns the `page_content` as context.
- Startup is kept lighter by loading the embedding backend lazily.

## Where indexing happens
- Manual/seed indexing: `scripts/seed.py` calls `get_rag_manager(...).index_store_data(..., force=True)` after creating sample data.
- There is no automatic re-index on product/description updates in the webhook/setup flows—updates must call indexing explicitly or be added later.

## How chat uses RAG
- `AIService.chat_stream()` pre-fetches RAG context for the user message and appends it to the prompt as `[Knowledge Base Context]`.
- The RAG import is lazy so chat still starts even if the embedding/vector extras are unavailable locally.
- For count queries ("how many"), the service also invokes `DatabaseTools.count_products()` and appends `[Live Database Status]` to the prompt.

## Data split
- PostgreSQL: users, stores, configuration, webhooks, platform tokens (encrypted), and vector storage via PGVector.
- No ChromaDB dependency in the current implementation.

## Important notes / Recommendations
- Add indexed update triggers (on product/description changes) or a background job to keep PGVector in sync.
- Consider storing metadata IDs with vectors so replies can include product references/citations.
- If you want true tool-driven streaming (agent runs tools live and streams results), implement a structured agent loop that can call tools and stream intermediate outputs.

## Naming Status
- Current active router is `app/routes/store.py` with `/api/store` endpoints.
- The old `business` router was removed; the codebase should use `store` terminology going forward.
- Some webhook/setup parameter names still use `store_id` already; docs should stay aligned with that.

---

File generated for quick context in conversations and developer onboarding.
