from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.config import get_settings
from app.core.database import get_db_session
from app.models.schemas import OAuthConnectionResponse, OAuthStartResponse
from app.services.oauth_client import build_authorization_url, exchange_code, generate_state, get_identity
from app.services.oauth_store import list_connections, pop_oauth_state, save_oauth_state, upsert_connection

router = APIRouter(prefix="/oauth", tags=["oauth"])
settings = get_settings()
SUPPORTED = {"github", "gitlab", "bitbucket"}


@router.get("/{provider}/start", response_model=OAuthStartResponse)
async def oauth_start(
    provider: str,
    user: dict = Depends(get_current_user),
) -> OAuthStartResponse:
    if provider not in SUPPORTED:
        raise HTTPException(status_code=404, detail="Unsupported provider")

    if not getattr(settings, f"{provider}_client_id", ""):
        raise HTTPException(status_code=500, detail=f"{provider} OAuth not configured")

    state = generate_state()
    await save_oauth_state(state, user["sub"], provider)
    return OAuthStartResponse(authorization_url=build_authorization_url(provider, state))


@router.get("/{provider}/callback")
async def oauth_callback(
    provider: str,
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db_session),
):
    if provider not in SUPPORTED:
        raise HTTPException(status_code=404, detail="Unsupported provider")

    state_payload = await pop_oauth_state(state)
    if not state_payload or state_payload.get("provider") != provider:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    token = await exchange_code(provider, code)
    access_token = token.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access token")

    account_id, username = await get_identity(provider, access_token)
    scopes = token.get("scope", "").split() if isinstance(token.get("scope"), str) else []

    await upsert_connection(
        db,
        user_id=state_payload["user_id"],
        provider=provider,
        account_id=account_id,
        username=username,
        access_token=access_token,
        refresh_token=token.get("refresh_token"),
        expires_in=token.get("expires_in"),
        scopes=scopes,
    )

    success_url = f"{settings.oauth_frontend_success_url}?connected={quote(provider)}"
    return RedirectResponse(success_url, status_code=302)


@router.get("/connections", response_model=list[OAuthConnectionResponse])
async def oauth_connections(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[OAuthConnectionResponse]:
    rows = await list_connections(db, user["sub"])
    return [OAuthConnectionResponse(**row) for row in rows]
