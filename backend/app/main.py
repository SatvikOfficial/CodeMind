from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.collaboration import router as collaboration_router
from app.api.health import router as health_router
from app.api.integrations import router as integrations_router
from app.api.oauth import router as oauth_router
from app.api.rules import router as rules_router
from app.api.ws import router as ws_router
from app.core.config import get_settings
from app.core.security import RateLimitMiddleware, SecurityHeadersMiddleware

settings = get_settings()
app = FastAPI(title="CodeMind Backend", version="1.0.0")
app.add_middleware(RateLimitMiddleware, requests_per_minute=180)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(rules_router)
app.include_router(integrations_router)
app.include_router(oauth_router)
app.include_router(collaboration_router)
app.include_router(ws_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "codemind-backend", "status": "running"}
