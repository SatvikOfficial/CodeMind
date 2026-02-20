import uuid
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rule_engine import Rule


async def list_rules(session: AsyncSession, user_id: str) -> list[Rule]:
    response = await session.execute(
        text(
            """
            SELECT id::text, name, pattern, message, severity, enabled
            FROM user_rules
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            """
        ),
        {"user_id": user_id},
    )
    return [Rule(**dict(row._mapping)) for row in response]


async def create_rule(session: AsyncSession, user_id: str, payload: dict[str, Any]) -> Rule:
    rule_id = str(uuid.uuid4())
    await session.execute(
        text(
            """
            INSERT INTO user_rules(id, user_id, name, pattern, message, severity, enabled)
            VALUES(:id::uuid, :user_id, :name, :pattern, :message, :severity, true)
            """
        ),
        {
            "id": rule_id,
            "user_id": user_id,
            "name": payload["name"],
            "pattern": payload["pattern"],
            "message": payload["message"],
            "severity": payload["severity"],
        },
    )
    await session.commit()
    return Rule(id=rule_id, enabled=True, **payload)


async def save_feedback(session: AsyncSession, user_id: str, payload: dict[str, Any]) -> None:
    await session.execute(
        text(
            """
            INSERT INTO feedback_events(id, user_id, analysis_id, accepted, note)
            VALUES(gen_random_uuid(), :user_id, :analysis_id::uuid, :accepted, :note)
            """
        ),
        {
            "user_id": user_id,
            "analysis_id": payload["analysis_id"],
            "accepted": payload["accepted"],
            "note": payload.get("note"),
        },
    )
    await session.commit()
