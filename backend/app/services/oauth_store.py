import json
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.redis_client import redis


async def save_oauth_state(state: str, user_id: str, provider: str) -> None:
    payload = json.dumps({"user_id": user_id, "provider": provider})
    await redis.set(f"oauth:state:{state}", payload, ex=600)


async def pop_oauth_state(state: str) -> dict[str, Any] | None:
    key = f"oauth:state:{state}"
    payload = await redis.get(key)
    if not payload:
        return None
    await redis.delete(key)
    return json.loads(payload)


async def upsert_connection(
    session: AsyncSession,
    user_id: str,
    provider: str,
    account_id: str,
    username: str,
    access_token: str,
    refresh_token: str | None,
    expires_in: int | None,
    scopes: list[str],
) -> None:
    expires_at = None
    if expires_in:
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    await session.execute(
        text(
            """
            INSERT INTO oauth_connections
              (id, user_id, provider, account_id, username, access_token, refresh_token, expires_at, scopes)
            VALUES
              (gen_random_uuid(), :user_id, :provider, :account_id, :username, :access_token, :refresh_token, :expires_at, :scopes::jsonb)
            ON CONFLICT (user_id, provider)
            DO UPDATE SET
              account_id = EXCLUDED.account_id,
              username = EXCLUDED.username,
              access_token = EXCLUDED.access_token,
              refresh_token = EXCLUDED.refresh_token,
              expires_at = EXCLUDED.expires_at,
              scopes = EXCLUDED.scopes,
              updated_at = NOW()
            """
        ),
        {
            "user_id": user_id,
            "provider": provider,
            "account_id": account_id,
            "username": username,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
            "scopes": json.dumps(scopes),
        },
    )
    await session.commit()


async def list_connections(session: AsyncSession, user_id: str) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT provider, username, created_at AS connected_at
            FROM oauth_connections
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            """
        ),
        {"user_id": user_id},
    )
    return [dict(row._mapping) for row in response]


async def get_access_token(session: AsyncSession, user_id: str, provider: str) -> str | None:
    response = await session.execute(
        text(
            """
            SELECT access_token
            FROM oauth_connections
            WHERE user_id = :user_id AND provider = :provider
            """
        ),
        {"user_id": user_id, "provider": provider},
    )
    row = response.first()
    return row.access_token if row else None
