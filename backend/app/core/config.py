"""Application settings loaded from environment variables / .env."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://stateside:stateside@db:5432/stateside"
    anthropic_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
