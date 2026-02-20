from fastapi import FastAPI

from app.engine import AIEngine
from app.models import CodeAnalysisRequest, CodeAnalysisResponse

app = FastAPI(title="CodeMind ML Service", version="1.0.0")
engine = AIEngine()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "ml-service"}


@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze(payload: CodeAnalysisRequest) -> CodeAnalysisResponse:
    data = await engine.analyze(payload.code, payload.language)
    return CodeAnalysisResponse(**data)
