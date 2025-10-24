"""Configuration management for Platzi News."""

import sentry_sdk
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from .core.exceptions import ConfigError


class Settings(BaseSettings):
    """Application settings using Pydantic for validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API Keys (required)
    guardian_api_key: str
    newsapi_api_key: str
    openai_api_key: str

    # Optional settings with defaults
    sentry_dsn: str | None = Field(None, description="Sentry DSN")
    max_articles: int = Field(10, description="Maximum number of articles to fetch")
    request_timeout: int = Field(10, description="Timeout for API requests in seconds")
    openai_model: str = Field("gpt-4", description="OpenAI model to use for analysis")
    openai_max_tokens: int = Field(
        500, description="Maximum tokens for OpenAI response"
    )


# Global settings instance with validation
try:
    settings = Settings()  # type: ignore[call-arg]
except ValidationError as e:
    missing_keys = [
        str(err["loc"][0]) for err in e.errors() if err["type"] == "missing"
    ]
    if missing_keys:
        msg = (
            "Las siguientes claves de API no están "
            f"configuradas: {', '.join(missing_keys)}. "
            "Por favor, configure las variables de entorno "
            "en un archivo .env o en su sistema."
        )
        raise ConfigError(msg) from e
    else:
        raise ConfigError(f"Error de configuración: {e}") from e

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/
        # for more info
        send_default_pii=True,
    )
