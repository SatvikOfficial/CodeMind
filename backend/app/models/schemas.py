from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = Field(default="typescript")
    repository: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class AnalyzeResponse(BaseModel):
    id: str
    suggestions: list[str]
    bugs: list[str]
    optimizations: list[str]
    documentation: str
    score: float
    created_at: datetime


class AnalysisSummary(BaseModel):
    id: str
    language: str
    repository: str | None = None
    score: float
    created_at: datetime


class AnalyticsResponse(BaseModel):
    total_analyses: int
    avg_score: float
    high_risk_count: int
    recent_languages: list[str]


class HealthResponse(BaseModel):
    status: str
    env: str


class FeedbackRequest(BaseModel):
    analysis_id: str
    accepted: bool
    note: str | None = None


class RuleCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    pattern: str = Field(min_length=1)
    message: str = Field(min_length=3)
    severity: str = Field(default="warning", pattern="^(info|warning|critical)$")


class RuleResponse(BaseModel):
    id: str
    name: str
    pattern: str
    message: str
    severity: str
    enabled: bool


class OAuthStartResponse(BaseModel):
    authorization_url: str


class OAuthConnectionResponse(BaseModel):
    provider: str
    username: str
    connected_at: datetime


class RepoIntegrationResponse(BaseModel):
    provider: str
    repositories: list[str]


class ReviewRoomCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    repository: str | None = None


class ReviewRoomParticipantRequest(BaseModel):
    user_id: str
    role: str = Field(pattern="^(owner|reviewer|viewer)$")


class ReviewRoomResponse(BaseModel):
    id: str
    name: str
    repository: str | None = None
    role: str
    created_at: datetime


class ReviewThreadCreateRequest(BaseModel):
    room_id: str
    title: str = Field(min_length=2)


class ReviewThreadResponse(BaseModel):
    id: str
    room_id: str
    title: str
    created_by: str
    created_at: datetime


class ReviewCommentCreateRequest(BaseModel):
    thread_id: str
    body: str = Field(min_length=1)
    parent_id: str | None = None
    mentions: list[str] = Field(default_factory=list)


class ReviewCommentResponse(BaseModel):
    id: str
    thread_id: str
    parent_id: str | None = None
    body: str
    author_id: str
    created_at: datetime


class NotificationResponse(BaseModel):
    id: str
    title: str
    body: str
    read: bool
    created_at: datetime
