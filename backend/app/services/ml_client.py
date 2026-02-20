from typing import Any

import httpx

from app.core.config import get_settings

settings = get_settings()


async def analyze_with_ml(payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{settings.ml_service_url}/analyze"
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
