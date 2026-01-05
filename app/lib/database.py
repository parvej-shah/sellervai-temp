from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.lib.config import settings

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import os

def sanitize_db_url(url: str) -> str:
    """Strip sslmode and other incompatible params for asyncpg."""
    if not url:
        return url
    
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    
    # List of parameters to remove for asyncpg compatibility
    # asyncpg doesn't support many standard libpq parameters via connection string
    incompatible_params = [
        'sslmode', 'sslrootcert', 'sslcert', 'sslkey', 
        'target_session_attrs', 'channel_binding', 
        'application_name', 'connect_timeout'
    ]
    
    for param in incompatible_params:
        query.pop(param, None)
    
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

# Create async engine with sanitized URL
engine = create_async_engine(
    sanitize_db_url(settings.DATABASE_URL),
    echo= False, # settings.ENVIRONMENT == "development",
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
