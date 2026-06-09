from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.lib.database import get_db
from app.models.models import User
from app.schemas.schemas import Token, UserResponse, TokenData, UserCreate
from app.lib.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash
)
from app.lib.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token (Form Data)."""
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


@router.post("/login/docs", response_model=Token)
async def login_docs(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Login endpoint specifically for documentation/Swagger UI."""
    return await login(username, password, db)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout (client should delete the token)."""
    return {
        "message": "Successfully logged out"
    }


@router.get("/session", response_model=UserResponse)
async def get_session(current_user: User = Depends(get_current_user)):
    """Get current user session/profile."""
    return current_user


# ---------------------------------------------------------------------------
# Google OAuth
# ---------------------------------------------------------------------------

class GoogleAuthRequest(BaseModel):
    """Payload sent by the frontend after Google Sign-In resolves."""
    email: str
    name: str
    google_id: str  # Google's stable 'sub' field from the decoded credential


@router.post("/google", response_model=Token, tags=["Authentication"])
async def google_auth(
    payload: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Exchange Google credentials for an app JWT.

    Frontend flow:
      1. Load Google Identity Services (GSI) via CDN.
      2. Call google.accounts.id.initialize({ client_id, callback }).
      3. In the callback, decode the credential JWT (base64 decode the payload).
      4. POST { email, name, google_id } to this endpoint.
      5. Store the returned access_token in localStorage and redirect to /dashboard.
    """
    # 1. Try lookup by google_id (fast path for returning users)
    result = await db.execute(select(User).filter(User.google_id == payload.google_id))
    user = result.scalar_one_or_none()

    if not user:
        # 2. Try lookup by email — link existing password account or create new
        result = await db.execute(select(User).filter(User.email == payload.email))
        user = result.scalar_one_or_none()

        if user:
            # Link Google ID to the existing account
            user.google_id = payload.google_id
        else:
            # Brand-new Google-only account (no password)
            user = User(
                name=payload.name,
                email=payload.email,
                google_id=payload.google_id,
                hashed_password=None,
            )
            db.add(user)

        await db.commit()
        await db.refresh(user)

    # 3. Issue standard app JWT
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
