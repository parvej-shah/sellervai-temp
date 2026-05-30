import os
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import aiofiles

from app.lib.database import get_db
from app.models.models import User, Store, StoreDocument, DocumentStatus
from app.schemas.schemas import StoreDocumentResponse
from app.lib.auth import get_current_user
from app.lib.rag import get_rag_manager
from app.lib.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/store", tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv", ".md"}


@router.post("/{store_id}/documents", response_model=StoreDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    store_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a document (PDF, TXT, DOCX, CSV, MD) to a store for RAG indexing."""
    
    # Verify store ownership
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Check file size
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Save file to disk
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(store_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
    
    # Create document record
    doc = StoreDocument(
        store_id=store_id,
        filename=file.filename,
        file_type=ext.lstrip("."),
        file_size=file_size,
        status=DocumentStatus.PROCESSING,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    
    # Index into RAG
    try:
        rag_manager = get_rag_manager(str(store_id))
        chunk_count = await rag_manager.index_file(file_path, file.filename)
        
        doc.status = DocumentStatus.INDEXED
        doc.chunk_count = chunk_count
        await db.commit()
        await db.refresh(doc)
        
        logger.info(f"Document '{file.filename}' indexed successfully ({chunk_count} chunks) for store {store_id}")
    except Exception as e:
        logger.error(f"Failed to index document '{file.filename}': {e}")
        doc.status = DocumentStatus.FAILED
        await db.commit()
        await db.refresh(doc)
        raise HTTPException(
            status_code=500,
            detail=f"File uploaded but indexing failed: {str(e)}"
        )
    
    return doc


@router.get("/{store_id}/documents", response_model=List[StoreDocumentResponse])
async def list_documents(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all documents uploaded to a store."""
    
    # Verify store ownership
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    result = await db.execute(
        select(StoreDocument).filter(StoreDocument.store_id == store_id).order_by(StoreDocument.created_at.desc())
    )
    documents = result.scalars().all()
    return documents


@router.delete("/{store_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    store_id: UUID,
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a document from the store."""
    
    # Verify store ownership
    result = await db.execute(
        select(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        )
    )
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    result = await db.execute(
        select(StoreDocument).filter(
            StoreDocument.id == document_id,
            StoreDocument.store_id == store_id
        )
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from disk
    file_path = os.path.join(settings.UPLOAD_DIR, str(store_id), doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    await db.delete(doc)
    await db.commit()
    
    return None
