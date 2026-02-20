from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db_session
from app.models.schemas import (
    NotificationResponse,
    ReviewCommentCreateRequest,
    ReviewCommentResponse,
    ReviewRoomCreateRequest,
    ReviewRoomParticipantRequest,
    ReviewRoomResponse,
    ReviewThreadCreateRequest,
    ReviewThreadResponse,
)
from app.services.collaboration_store import (
    add_participant,
    create_comment,
    create_notifications_for_room,
    create_room,
    create_thread,
    get_room_id_by_thread,
    get_user_role,
    list_comments,
    list_notifications,
    list_rooms,
    list_threads,
    mark_notification_read,
)

router = APIRouter(prefix="/collaboration", tags=["collaboration"])


def _can_write(role: str | None) -> bool:
    return role in {"owner", "reviewer"}


@router.post("/rooms", response_model=ReviewRoomResponse)
async def post_room(
    payload: ReviewRoomCreateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ReviewRoomResponse:
    room = await create_room(db, user["sub"], payload.name, payload.repository)
    return ReviewRoomResponse(**room)


@router.get("/rooms", response_model=list[ReviewRoomResponse])
async def get_rooms(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[ReviewRoomResponse]:
    rows = await list_rooms(db, user["sub"])
    return [ReviewRoomResponse(**row) for row in rows]


@router.post("/rooms/{room_id}/participants")
async def post_participant(
    room_id: str,
    payload: ReviewRoomParticipantRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    role = await get_user_role(db, room_id, user["sub"])
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can update participants")

    await add_participant(db, room_id, payload.user_id, payload.role)
    return {"status": "updated"}


@router.post("/threads", response_model=ReviewThreadResponse)
async def post_thread(
    payload: ReviewThreadCreateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ReviewThreadResponse:
    role = await get_user_role(db, payload.room_id, user["sub"])
    if not _can_write(role):
        raise HTTPException(status_code=403, detail="Insufficient role")

    thread = await create_thread(db, payload.room_id, payload.title, user["sub"])
    await create_notifications_for_room(db, payload.room_id, user["sub"], "New review thread", payload.title)
    return ReviewThreadResponse(**thread)


@router.get("/rooms/{room_id}/threads", response_model=list[ReviewThreadResponse])
async def get_threads(
    room_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[ReviewThreadResponse]:
    role = await get_user_role(db, room_id, user["sub"])
    if not role:
        raise HTTPException(status_code=403, detail="Not a participant")

    rows = await list_threads(db, room_id)
    return [ReviewThreadResponse(**row) for row in rows]


@router.post("/comments", response_model=ReviewCommentResponse)
async def post_comment(
    payload: ReviewCommentCreateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ReviewCommentResponse:
    room_id = await get_room_id_by_thread(db, payload.thread_id)
    role = await get_user_role(db, room_id, user["sub"])
    if not _can_write(role):
        raise HTTPException(status_code=403, detail="Insufficient role")

    comment = await create_comment(db, payload.thread_id, user["sub"], payload.body, payload.parent_id)
    await create_notifications_for_room(db, room_id, user["sub"], "New review comment", payload.body[:120])
    return ReviewCommentResponse(**comment)


@router.get("/threads/{thread_id}/comments", response_model=list[ReviewCommentResponse])
async def get_comments(
    thread_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[ReviewCommentResponse]:
    room_id = await get_room_id_by_thread(db, thread_id)
    role = await get_user_role(db, room_id, user["sub"])
    if not role:
        raise HTTPException(status_code=403, detail="Not a participant")

    rows = await list_comments(db, thread_id)
    return [ReviewCommentResponse(**row) for row in rows]


@router.get("/notifications", response_model=list[NotificationResponse])
async def get_user_notifications(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[NotificationResponse]:
    rows = await list_notifications(db, user["sub"])
    return [NotificationResponse(**row) for row in rows]


@router.post("/notifications/{notification_id}/read")
async def read_notification(
    notification_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    await mark_notification_read(db, notification_id, user["sub"])
    return {"status": "updated"}
