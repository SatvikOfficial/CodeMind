import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def save_analysis(
    session: AsyncSession,
    user_id: str,
    payload: dict[str, Any],
    result: dict[str, Any],
) -> str:
    query = text(
        """
        INSERT INTO analysis_reports
        (id, user_id, language, repository, code, suggestions, bugs, optimizations, documentation, score)
        VALUES
        (gen_random_uuid(), :user_id, :language, :repository, :code, :suggestions::jsonb, :bugs::jsonb, :optimizations::jsonb, :documentation, :score)
        RETURNING id::text
        """
    )
    response = await session.execute(
        query,
        {
            "user_id": user_id,
            "language": payload.get("language", "unknown"),
            "repository": payload.get("repository"),
            "code": payload.get("code", ""),
            "suggestions": json.dumps(result.get("suggestions", [])),
            "bugs": json.dumps(result.get("bugs", [])),
            "optimizations": json.dumps(result.get("optimizations", [])),
            "documentation": result.get("documentation", ""),
            "score": float(result.get("score", 0)),
        },
    )
    created_id = response.scalar_one()
    await session.commit()
    return created_id


async def get_analytics(session: AsyncSession, user_id: str) -> dict[str, Any]:
    totals = await session.execute(
        text(
            """
            SELECT COUNT(*)::int AS total_analyses,
                   COALESCE(AVG(score), 0)::float AS avg_score,
                   COUNT(*) FILTER (WHERE score < 0.5)::int AS high_risk_count
            FROM analysis_reports
            WHERE user_id = :user_id
            """
        ),
        {"user_id": user_id},
    )

    languages = await session.execute(
        text(
            """
            SELECT language
            FROM analysis_reports
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 5
            """
        ),
        {"user_id": user_id},
    )

    row = totals.one()
    return {
        "total_analyses": row.total_analyses,
        "avg_score": row.avg_score,
        "high_risk_count": row.high_risk_count,
        "recent_languages": [r.language for r in languages],
    }


async def get_recent_reports(session: AsyncSession, user_id: str, limit: int = 10) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT id::text, language, repository, score, created_at
            FROM analysis_reports
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT :limit
            """
        ),
        {"user_id": user_id, "limit": limit},
    )
    return [dict(row._mapping) for row in response]
