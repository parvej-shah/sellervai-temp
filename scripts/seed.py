import asyncio
import uuid
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.database import AsyncSessionLocal
from app.models.models import User, Business, ServiceStatus, WebhookStatus
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

        # 2. Create a test business
        business_name = "Tech Gadgets Pro"
        result = await session.execute(
            select(Business).filter(Business.user_id == user.id, Business.name == business_name)
        )
        business = result.scalar_one_or_none()
        
        if not business:
            print(f"Creating business: {business_name}")
            business = Business(
                id=uuid.uuid4(),
                user_id=user.id,
                name=business_name,
                description="A high-end electronics store specializing in the latest gadgets and accessories.",
                products_items=[
                    {"name": "UltraPhone 15", "description": "Flagship smartphone with 8K camera.", "price": 999},
                    {"name": "NanoWatch v2", "description": "Smartwatch with health tracking.", "price": 299},
                    {"name": "SoundMax Pro", "description": "Noise-cancelling wireless headphones.", "price": 199}
                ]
            )
            session.add(business)
        else:
            print(f"Business {business_name} already exists.")

        await session.commit()
        
        # 3. Index data into RAG
        print(f"Indexing RAG for business: {business.name}...")
        rag_manager = get_rag_manager(str(business.id))
        await rag_manager.index_business_data(business.description, business.products_items, force=True)
        
        print("Seeding and RAG Indexing completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
