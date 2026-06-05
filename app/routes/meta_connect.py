from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import httpx
import logging

from app.lib.database import get_db
from app.models.models import User, Store, ConnectedPage, ConnectedInstagram, ConnectedWhatsapp
from app.lib.auth import get_current_user
from app.lib.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/meta", tags=["Meta Connect"])


@router.post("/connect-facebook/{store_id}")
async def connect_facebook(
    store_id: UUID,
    payload: dict, # Expects {"user_access_token": "...", "connect_instagram": bool}
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Connect Facebook pages using a user access token obtained from the frontend.
    """
    user_access_token = payload.get("user_access_token")
    connect_instagram = payload.get("connect_instagram", False)
    
    if not user_access_token:
        raise HTTPException(status_code=400, detail="Missing user_access_token")
        
    # Verify store ownership
    result = await db.execute(select(Store).filter(Store.id == store_id, Store.user_id == current_user.id))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
        
    async with httpx.AsyncClient() as client:
        # Exchange for long-lived token
        if settings.META_APP_ID and settings.META_APP_SECRET:
            ll_url = f"https://graph.facebook.com/v25.0/oauth/access_token?grant_type=fb_exchange_token&client_id={settings.META_APP_ID}&client_secret={settings.META_APP_SECRET}&fb_exchange_token={user_access_token}"
            ll_resp = await client.get(ll_url)
            ll_data = ll_resp.json()
            if "access_token" in ll_data:
                user_access_token = ll_data["access_token"]

        # Get Pages
        pages_url = f"https://graph.facebook.com/v25.0/me/accounts?fields=id,name,access_token&access_token={user_access_token}"
        resp = await client.get(pages_url)
        data = resp.json()
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"].get("message", "Error fetching pages"))
            
        pages = data.get("data", [])
        connected_pages_list = []
        
        for page in pages:
            page_id = page["id"]
            page_token = page["access_token"]
            
            # Subscribe webhook
            sub_url = f"https://graph.facebook.com/v25.0/{page_id}/subscribed_apps"
            sub_payload = {"subscribed_fields": "messages,messaging_postbacks,feed,pages_read_engagement,pages_manage_posts,public_profile", "access_token": page_token}
            await client.post(sub_url, data=sub_payload)
            
            # Save to DB
            p_res = await db.execute(select(ConnectedPage).filter(ConnectedPage.page_id == page_id))
            existing_page = p_res.scalar_one_or_none()
            if existing_page:
                existing_page.token = page_token
                existing_page.store_id = store_id
                existing_page.user_id = current_user.id
                existing_page.page_name = page.get("name")
            else:
                new_page = ConnectedPage(
                    store_id=store_id,
                    user_id=current_user.id,
                    page_id=page_id,
                    page_name=page.get("name"),
                    token=page_token
                )
                db.add(new_page)
                
            connected_pages_list.append(page_id)
            
            if connect_instagram:
                # Get IG account
                ig_url = f"https://graph.facebook.com/v25.0/{page_id}?fields=instagram_business_account{{id,username}}&access_token={page_token}"
                ig_resp = await client.get(ig_url)
                ig_data = ig_resp.json()
                
                ig_account = ig_data.get("instagram_business_account")
                if ig_account:
                    ig_user_id = ig_account["id"]
                    ig_username = ig_account.get("username")
                    
                    # Subscribe IG webhook
                    ig_sub_url = f"https://graph.facebook.com/v25.0/{ig_user_id}/subscribed_apps"
                    ig_sub_payload = {"subscribed_fields": "messages,comments,feed,pages_read_engagement,pages_manage_posts,public_profile", "access_token": page_token}
                    await client.post(ig_sub_url, data=ig_sub_payload)
                    
                    # Save to DB
                    ig_res = await db.execute(select(ConnectedInstagram).filter(ConnectedInstagram.ig_user_id == ig_user_id))
                    existing_ig = ig_res.scalar_one_or_none()
                    if existing_ig:
                        existing_ig.token = page_token
                        existing_ig.store_id = store_id
                        existing_ig.ig_username = ig_username
                    else:
                        new_ig = ConnectedInstagram(
                            store_id=store_id,
                            ig_user_id=ig_user_id,
                            ig_username=ig_username,
                            token=page_token
                        )
                        db.add(new_ig)
                        
        await db.commit()
        return {"status": "success", "connected_pages": connected_pages_list}


@router.post("/connect-whatsapp/{store_id}")
async def connect_whatsapp(
    store_id: UUID,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Connect WhatsApp via Embedded Signup (OAuth flow).
    """
    code = payload.get("code")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing required 'code' parameter")
        
    result = await db.execute(select(Store).filter(Store.id == store_id, Store.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
        
    async with httpx.AsyncClient() as client:
        # Exchange code for token
        token_url = f"https://graph.facebook.com/v25.0/oauth/access_token?client_id={settings.META_APP_ID}&client_secret={settings.META_APP_SECRET}&code={code}"
        token_res = await client.get(token_url)
        token_data = token_res.json()
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"].get("message", "Error exchanging code for token"))
            
        user_token = token_data.get("access_token")

        # Get WABA ID
        waba_url = f"https://graph.facebook.com/v25.0/me/businesses?access_token={user_token}"
        waba_res = await client.get(waba_url)
        waba_data = waba_res.json()
        if not waba_data.get("data"):
            raise HTTPException(status_code=400, detail="No WhatsApp Business Account found")
        waba_id = waba_data["data"][0]["id"]

        # Get phone number ID
        phone_url = f"https://graph.facebook.com/v25.0/{waba_id}/phone_numbers?fields=id,display_phone_number&access_token={user_token}"
        phone_res = await client.get(phone_url)
        phone_data = phone_res.json()
        if not phone_data.get("data"):
            raise HTTPException(status_code=400, detail="No Phone Number found for WABA")
        phone_number_id = phone_data["data"][0]["id"]
        phone_name = phone_data["data"][0].get("display_phone_number")
        
        # Subscribe webhook
        sub_url = f"https://graph.facebook.com/v25.0/{waba_id}/subscribed_apps"
        sub_payload = {"access_token": user_token}
        await client.post(sub_url, data=sub_payload)
        
        wa_res = await db.execute(select(ConnectedWhatsapp).filter(ConnectedWhatsapp.phone_number_id == phone_number_id))
        existing_wa = wa_res.scalar_one_or_none()
        if existing_wa:
            existing_wa.waba_id = waba_id
            existing_wa.token = user_token
            existing_wa.store_id = store_id
            existing_wa.name = phone_name
        else:
            new_wa = ConnectedWhatsapp(
                store_id=store_id,
                waba_id=waba_id,
                phone_number_id=phone_number_id,
                name=phone_name,
                token=user_token
            )
            db.add(new_wa)
            
        await db.commit()
        return {"status": "success"}


@router.delete("/disconnect-facebook/{store_id}/{page_id}")
async def disconnect_facebook(
    store_id: UUID,
    page_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Store).filter(Store.id == store_id, Store.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
        
    p_res = await db.execute(select(ConnectedPage).filter(ConnectedPage.page_id == page_id, ConnectedPage.store_id == store_id))
    page = p_res.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Connected page not found")
        
    async with httpx.AsyncClient() as client:
        # Delete subscription
        sub_url = f"https://graph.facebook.com/v25.0/{page_id}/subscribed_apps"
        await client.delete(sub_url, params={"access_token": page.token})
        
    await db.delete(page)
    await db.commit()
    return {"status": "success"}

@router.delete("/disconnect-instagram/{store_id}/{ig_user_id}")
async def disconnect_instagram(
    store_id: UUID,
    ig_user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Store).filter(Store.id == store_id, Store.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
        
    p_res = await db.execute(select(ConnectedInstagram).filter(ConnectedInstagram.ig_user_id == ig_user_id, ConnectedInstagram.store_id == store_id))
    page = p_res.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Connected Instagram not found")
        
    async with httpx.AsyncClient() as client:
        sub_url = f"https://graph.facebook.com/v25.0/{ig_user_id}/subscribed_apps"
        await client.delete(sub_url, params={"access_token": page.token})
        
    await db.delete(page)
    await db.commit()
    return {"status": "success"}

@router.delete("/disconnect-whatsapp/{store_id}/{phone_number_id}")
async def disconnect_whatsapp(
    store_id: UUID,
    phone_number_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Store).filter(Store.id == store_id, Store.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
        
    p_res = await db.execute(select(ConnectedWhatsapp).filter(ConnectedWhatsapp.phone_number_id == phone_number_id, ConnectedWhatsapp.store_id == store_id))
    page = p_res.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Connected WhatsApp not found")
        
    async with httpx.AsyncClient() as client:
        sub_url = f"https://graph.facebook.com/v25.0/{page.waba_id}/subscribed_apps"
        await client.delete(sub_url, params={"access_token": page.token})
        
    await db.delete(page)
    await db.commit()
    return {"status": "success"}


# ============================================================================
# Get Connected Pages and Accounts
# ============================================================================

@router.get("/connected-pages/{store_id}")
async def get_connected_pages(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all connected Facebook pages for a store."""
    # Verify store ownership
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Get connected pages
    pages_result = await db.execute(
        select(ConnectedPage).filter(ConnectedPage.store_id == store_id)
    )
    pages = pages_result.scalars().all()
    
    return {
        "pages": [
            {
                "page_id": page.page_id,
                "page_name": page.page_name or page.page_id,
                "token": page.token,
            }
            for page in pages
        ]
    }


@router.get("/connected-instagram/{store_id}")
async def get_connected_instagram(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all connected Instagram accounts for a store."""
    # Verify store ownership
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Get connected Instagram accounts
    ig_result = await db.execute(
        select(ConnectedInstagram).filter(ConnectedInstagram.store_id == store_id)
    )
    accounts = ig_result.scalars().all()
    
    return {
        "accounts": [
            {
                "ig_user_id": account.ig_user_id,
                "ig_username": account.ig_username or account.ig_user_id,
                "token": account.token,
            }
            for account in accounts
        ]
    }

@router.get("/connected-whatsapp/{store_id}")
async def get_connected_whatsapp(
    store_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all connected WhatsApp accounts for a store."""
    result = await db.execute(
        select(Store).filter(Store.id == store_id, Store.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Store not found")
    
    wa_result = await db.execute(
        select(ConnectedWhatsapp).filter(ConnectedWhatsapp.store_id == store_id)
    )
    accounts = wa_result.scalars().all()
    
    return {
        "accounts": [
            {
                "phone_number_id": account.phone_number_id,
                "name": account.name or account.phone_number_id,
                "waba_id": account.waba_id,
                "token": account.token,
            }
            for account in accounts
        ]
    }

