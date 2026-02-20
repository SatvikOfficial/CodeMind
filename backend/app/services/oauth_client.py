import base64
import secrets
from urllib.parse import urlencode

import httpx

from app.core.config import get_settings

settings = get_settings()

PROVIDERS = {
    "github": {
        "authorize": "https://github.com/login/oauth/authorize",
        "token": "https://github.com/login/oauth/access_token",
        "scope": "repo read:user",
    },
    "gitlab": {
        "authorize": "https://gitlab.com/oauth/authorize",
        "token": "https://gitlab.com/oauth/token",
        "scope": "read_user read_api",
    },
    "bitbucket": {
        "authorize": "https://bitbucket.org/site/oauth2/authorize",
        "token": "https://bitbucket.org/site/oauth2/access_token",
        "scope": "repository account",
    },
}


def callback_url(provider: str) -> str:
    return f"{settings.oauth_redirect_base}/oauth/{provider}/callback"


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def build_authorization_url(provider: str, state: str) -> str:
    if provider not in PROVIDERS:
        raise ValueError("Unsupported provider")

    client_id = getattr(settings, f"{provider}_client_id", "")
    params = {
        "client_id": client_id,
        "redirect_uri": callback_url(provider),
        "response_type": "code",
        "state": state,
        "scope": PROVIDERS[provider]["scope"],
    }
    return f"{PROVIDERS[provider]['authorize']}?{urlencode(params)}"


async def exchange_code(provider: str, code: str) -> dict:
    redirect_uri = callback_url(provider)
    client_id = getattr(settings, f"{provider}_client_id", "")
    client_secret = getattr(settings, f"{provider}_client_secret", "")

    async with httpx.AsyncClient(timeout=20.0) as client:
        if provider == "bitbucket":
            raw = f"{client_id}:{client_secret}".encode()
            basic = base64.b64encode(raw).decode()
            response = await client.post(
                PROVIDERS[provider]["token"],
                headers={"Authorization": f"Basic {basic}"},
                data={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri},
            )
        elif provider == "gitlab":
            response = await client.post(
                PROVIDERS[provider]["token"],
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                },
            )
        else:
            response = await client.post(
                PROVIDERS[provider]["token"],
                headers={"Accept": "application/json"},
                json={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
            )

    response.raise_for_status()
    return response.json()


async def get_identity(provider: str, access_token: str) -> tuple[str, str]:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        if provider == "github":
            response = await client.get("https://api.github.com/user", headers=headers)
            response.raise_for_status()
            data = response.json()
            return str(data["id"]), data["login"]

        if provider == "gitlab":
            response = await client.get("https://gitlab.com/api/v4/user", headers=headers)
            response.raise_for_status()
            data = response.json()
            return str(data["id"]), data["username"]

        response = await client.get("https://api.bitbucket.org/2.0/user", headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["account_id"], data["username"]
