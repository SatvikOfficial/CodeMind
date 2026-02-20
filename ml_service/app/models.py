from typing import Any

from pydantic import BaseModel, Field


class CodeAnalysisRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = Field(default="typescript")
    context: dict[str, Any] = Field(default_factory=dict)
    repository: str | None = None


class CodeAnalysisResponse(BaseModel):
    suggestions: list[str]
    bugs: list[str]
    optimizations: list[str]
    documentation: str
    score: float
    embedding: list[float]
