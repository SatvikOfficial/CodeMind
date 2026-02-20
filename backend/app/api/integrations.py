from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db_session
from app.models.schemas import RepoIntegrationResponse
from app.services.git_providers import list_bitbucket_repos, list_github_repos, list_gitlab_repos
from app.services.oauth_store import get_access_token

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/{provider}/repos", response_model=RepoIntegrationResponse)
async def repos(
    provider: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> RepoIntegrationResponse:
    token = await get_access_token(db, user_id=user["sub"], provider=provider)
    if not token:
        raise HTTPException(status_code=404, detail=f"No OAuth connection found for {provider}")

    if provider == "github":
        repositories = await list_github_repos(token)
    elif provider == "gitlab":
        repositories = await list_gitlab_repos(token)
    elif provider == "bitbucket":
        repositories = await list_bitbucket_repos(token)
    else:
        raise HTTPException(status_code=404, detail="Provider not supported")

    return RepoIntegrationResponse(provider=provider, repositories=repositories)
