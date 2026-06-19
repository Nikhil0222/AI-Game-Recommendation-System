from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GAMEMIND_",
        extra="ignore",
    )

    env: str = "local"
    log_level: str = "INFO"
    openai_api_key: str | None = None
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    use_local_embeddings: bool = True
    use_local_ranker: bool = True
    dataset_path: Path = Field(default=Path("data/sample_games.jsonl"))
    chroma_path: Path = Field(default=Path(".chroma"))
    chroma_collection: str = "games"
    embedding_dimensions: int = 384
    default_recommendation_count: int = 5
    max_recommendation_count: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
