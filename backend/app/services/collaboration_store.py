from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def create_room(session: AsyncSession, user_id: str, name: str, repository: str | None) -> dict[str, Any]:
    created = await session.execute(
        text(
            """
            INSERT INTO review_rooms(id, name, repository, created_by)
            VALUES (gen_random_uuid(), :name, :repository, :created_by)
            RETURNING id::text, name, repository, created_at
            """
        ),
        {"name": name, "repository": repository, "created_by": user_id},
    )
    room = dict(created.one()._mapping)
    await session.execute(
        text(
            """
            INSERT INTO review_participants(id, room_id, user_id, role)
            VALUES (gen_random_uuid(), :room_id::uuid, :user_id, 'owner')
            """
        ),
        {"room_id": room["id"], "user_id": user_id},
    )
    await session.commit()
    room["role"] = "owner"
    return room


async def list_rooms(session: AsyncSession, user_id: str) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT r.id::text, r.name, r.repository, p.role, r.created_at
            FROM review_rooms r
            JOIN review_participants p ON p.room_id = r.id
            WHERE p.user_id = :user_id
            ORDER BY r.created_at DESC
            """
        ),
        {"user_id": user_id},
    )
    return [dict(row._mapping) for row in response]


async def get_user_role(session: AsyncSession, room_id: str, user_id: str) -> str | None:
    response = await session.execute(
        text("SELECT role FROM review_participants WHERE room_id = :room_id::uuid AND user_id = :user_id"),
        {"room_id": room_id, "user_id": user_id},
    )
    row = response.first()
    return row.role if row else None


async def add_participant(session: AsyncSession, room_id: str, user_id: str, role: str) -> None:
    await session.execute(
        text(
            """
            INSERT INTO review_participants(id, room_id, user_id, role)
            VALUES (gen_random_uuid(), :room_id::uuid, :user_id, :role)
            ON CONFLICT (room_id, user_id)
            DO UPDATE SET role = EXCLUDED.role
            """
        ),
        {"room_id": room_id, "user_id": user_id, "role": role},
    )
    await session.commit()


async def create_thread(session: AsyncSession, room_id: str, title: str, user_id: str) -> dict[str, Any]:
    response = await session.execute(
        text(
            """
            INSERT INTO review_threads(id, room_id, title, created_by)
            VALUES (gen_random_uuid(), :room_id::uuid, :title, :created_by)
            RETURNING id::text, room_id::text, title, created_by, created_at
            """
        ),
        {"room_id": room_id, "title": title, "created_by": user_id},
    )
    await session.commit()
    return dict(response.one()._mapping)


async def list_threads(session: AsyncSession, room_id: str) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT id::text, room_id::text, title, created_by, created_at
            FROM review_threads
            WHERE room_id = :room_id::uuid
            ORDER BY created_at DESC
            """
        ),
        {"room_id": room_id},
    )
    return [dict(row._mapping) for row in response]


async def create_comment(
    session: AsyncSession,
    thread_id: str,
    user_id: str,
    body: str,
    parent_id: str | None,
) -> dict[str, Any]:
    response = await session.execute(
        text(
            """
            INSERT INTO review_comments(id, thread_id, parent_id, body, author_id)
            VALUES (gen_random_uuid(), :thread_id::uuid, :parent_id::uuid, :body, :author_id)
            RETURNING id::text, thread_id::text, parent_id::text, body, author_id, created_at
            """
        ),
        {"thread_id": thread_id, "parent_id": parent_id, "body": body, "author_id": user_id},
    )
    await session.commit()
    return dict(response.one()._mapping)


async def list_comments(session: AsyncSession, thread_id: str) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT id::text, thread_id::text, parent_id::text, body, author_id, created_at
            FROM review_comments
            WHERE thread_id = :thread_id::uuid
            ORDER BY created_at ASC
            """
        ),
        {"thread_id": thread_id},
    )
    return [dict(row._mapping) for row in response]


async def get_room_id_by_thread(session: AsyncSession, thread_id: str) -> str:
    response = await session.execute(
        text("SELECT room_id::text FROM review_threads WHERE id = :thread_id::uuid"),
        {"thread_id": thread_id},
    )
    row = response.first()
    return row.room_id if row else ""


async def create_notifications_for_room(session: AsyncSession, room_id: str, sender_id: str, title: str, body: str) -> None:
    users = await session.execute(
        text("SELECT user_id FROM review_participants WHERE room_id = :room_id::uuid AND user_id <> :sender"),
        {"room_id": room_id, "sender": sender_id},
    )
    for row in users:
        await session.execute(
            text(
                """
                INSERT INTO notifications(id, user_id, title, body, read)
                VALUES (gen_random_uuid(), :user_id, :title, :body, false)
                """
            ),
            {"user_id": row.user_id, "title": title, "body": body},
        )
    await session.commit()


async def list_notifications(session: AsyncSession, user_id: str) -> list[dict[str, Any]]:
    response = await session.execute(
        text(
            """
            SELECT id::text, title, body, read, created_at
            FROM notifications
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 50
            """
        ),
        {"user_id": user_id},
    )
    return [dict(row._mapping) for row in response]


async def mark_notification_read(session: AsyncSession, notification_id: str, user_id: str) -> None:
    await session.execute(
        text(
            """
            UPDATE notifications
            SET read = true
            WHERE id = :notification_id::uuid AND user_id = :user_id
            """
        ),
        {"notification_id": notification_id, "user_id": user_id},
    )
    await session.commit()
