import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db_session
from app.models.schemas import AnalysisSummary, AnalyticsResponse, AnalyzeRequest, AnalyzeResponse
from app.services.analysis_store import get_analytics, get_recent_reports, save_analysis
from app.services.ml_client import analyze_with_ml
from app.services.redis_client import redis
from app.services.rule_engine import apply_rules
from app.services.rule_store import list_rules

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalyzeResponse)
async def analyze_code(
    payload: AnalyzeRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AnalyzeResponse:
    cache_key = f"analysis:{hashlib.sha256((payload.code + payload.language).encode()).hexdigest()}"
    cached = await redis.get(cache_key)
    if cached:
        data = json.loads(cached)
        return AnalyzeResponse(**data)

    try:
        result = await analyze_with_ml(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"ML service unavailable: {exc}") from exc

    custom_rules = await list_rules(db, user_id=user["sub"])
    rule_findings = apply_rules(payload.code, custom_rules)
    if rule_findings:
        result["bugs"] = [*result.get("bugs", []), *rule_findings]
        result["score"] = max(0.0, float(result.get("score", 0.7)) - min(0.4, len(rule_findings) * 0.05))

    report_id = await save_analysis(db, user_id=user["sub"], payload=payload.model_dump(), result=result)
    response = AnalyzeResponse(
        id=report_id,
        suggestions=result.get("suggestions", []),
        bugs=result.get("bugs", []),
        optimizations=result.get("optimizations", []),
        documentation=result.get("documentation", ""),
        score=float(result.get("score", 0)),
        created_at=datetime.utcnow(),
    )
    await redis.set(cache_key, response.model_dump_json(), ex=300)
    return response


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AnalyticsResponse:
    data = await get_analytics(db, user_id=user["sub"])
    return AnalyticsResponse(**data)


@router.get("/recent", response_model=list[AnalysisSummary])
async def recent_reports(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[AnalysisSummary]:
    rows = await get_recent_reports(db, user_id=user["sub"], limit=12)
    return [AnalysisSummary(**row) for row in rows]
