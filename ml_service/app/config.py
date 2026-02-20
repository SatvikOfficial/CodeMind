from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    ml_port: int = 8001
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_api_key: str = ""
    nvidia_model: str = "meta/llama-3.1-70b-instruct"
    pinecone_api_key: str = ""
    pinecone_index: str = "codemind-code-embeddings"
    pinecone_host: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
