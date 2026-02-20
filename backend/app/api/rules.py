from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db_session
from app.models.schemas import FeedbackRequest, RuleCreateRequest, RuleResponse
from app.services.rule_store import create_rule, list_rules, save_feedback

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("", response_model=list[RuleResponse])
async def get_rules(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[RuleResponse]:
    rules = await list_rules(db, user_id=user["sub"])
    return [RuleResponse(**rule.__dict__) for rule in rules]


@router.post("", response_model=RuleResponse)
async def post_rule(
    payload: RuleCreateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> RuleResponse:
    rule = await create_rule(db, user_id=user["sub"], payload=payload.model_dump())
    return RuleResponse(**rule.__dict__)


@router.post("/feedback")
async def feedback(
    payload: FeedbackRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    await save_feedback(db, user_id=user["sub"], payload=payload.model_dump())
    return {"status": "saved"}
