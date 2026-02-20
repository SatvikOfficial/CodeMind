from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    api_port: int = 8000
    frontend_origin: str = "http://localhost:3000"
    database_url: str = "postgresql+asyncpg://codemind:codemind@localhost:5432/codemind"
    redis_url: str = "redis://localhost:6379/0"
    ml_service_url: str = "http://localhost:8001"
    clerk_issuer: str = ""
    clerk_jwks_url: str = ""
    clerk_optional_auth: bool = True
    oauth_redirect_base: str = "http://localhost:8000"
    oauth_frontend_success_url: str = "http://localhost:3000/integrations"
    github_client_id: str = ""
    github_client_secret: str = ""
    gitlab_client_id: str = ""
    gitlab_client_secret: str = ""
    bitbucket_client_id: str = ""
    bitbucket_client_secret: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
