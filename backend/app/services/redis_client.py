import json
from typing import Any

from app.core.config import get_settings

settings = get_settings()

try:
    from redis.asyncio import Redis

    redis = Redis.from_url(settings.redis_url, decode_responses=True)
except ModuleNotFoundError:
    class InMemoryRedis:
        def __init__(self) -> None:
            self.store: dict[str, str] = {}

        async def get(self, key: str) -> str | None:
            return self.store.get(key)

        async def set(self, key: str, value: str, ex: int | None = None) -> bool:
            self.store[key] = value if isinstance(value, str) else json.dumps(value)
            return True

        async def delete(self, key: str) -> int:
            existed = key in self.store
            if existed:
                del self.store[key]
            return 1 if existed else 0

    redis: Any = InMemoryRedis()
