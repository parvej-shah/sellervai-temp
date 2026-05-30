import asyncio
import uuid
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.database import AsyncSessionLocal
from app.models.models import User, Store, ServiceStatus, WebhookStatus
from app.lib.auth import get_password_hash
from app.lib.rag import get_rag_manager

async def seed_data():
    async with AsyncSessionLocal() as session:
        # 1. Create a test user
        user_email = "test@example.com"
        
        # Check if user already exists
        from sqlalchemy import select
        result = await session.execute(select(User).filter(User.email == user_email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Creating user: {user_email}")
            user = User(
                id=uuid.uuid4(),
                name="Test Professional",
                email=user_email,
                phone_number="+1234567890",
                hashed_password=get_password_hash("password")
            )
            session.add(user)
            await session.flush()
        else:
            print(f"User {user_email} already exists.")
            # Update password just in case
            user.hashed_password = get_password_hash("password")

        # 2. Create a test store
        store_name = "Tech Gadgets Pro"
        result = await session.execute(
            select(Store).filter(Store.user_id == user.id, Store.name == store_name)
        )
        store = result.scalar_one_or_none()
        
        if not store:
            print(f"Creating store: {store_name}")
            store = Store(
                id=uuid.uuid4(),
                user_id=user.id,
                name=store_name,
                description="A high-end electronics store specializing in the latest gadgets and accessories.",
                tone="friendly",
                personality_prompt="You are a knowledgeable tech expert who loves helping customers find the perfect gadget. Be enthusiastic but honest about product capabilities.",
                welcome_message="Welcome to Tech Gadgets Pro! 🎉 How can I help you find the perfect tech today?",
                language="english",
                products_items=[
                    {"name": "UltraPhone 15", "description": "Flagship smartphone with 8K camera.", "price": 999},
                    {"name": "NanoWatch v2", "description": "Smartwatch with health tracking.", "price": 299},
                    {"name": "SoundMax Pro", "description": "Noise-cancelling wireless headphones.", "price": 199}
                ]
            )
            session.add(store)
        else:
            print(f"Store {store_name} already exists.")

        await session.commit()
        
        # 3. Index data into RAG
        print(f"Indexing RAG for store: {store.name}...")
        rag_manager = get_rag_manager(str(store.id))
        await rag_manager.index_store_data(store.description, store.products_items, force=True)
        
        print("Seeding and RAG Indexing completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
