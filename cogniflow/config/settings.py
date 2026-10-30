"""Application configuration and environment variable validation."""

import os
from functools import lru_cache
from typing import Literal, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv(override=True)


class Settings(BaseModel):
    """Central configuration for LLM providers and runtime parameters."""

    default_provider: Literal["google", "openai", "groq"] = Field(
        default_factory=lambda: os.getenv("DEFAULT_LLM_PROVIDER", "google").lower()
    )

    google_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY")
    )

    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )

    groq_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("GROQ_API_KEY")
    )

    # Model Defaults
    google_default_model: str = "gemini-1.5-flash"
    openai_default_model: str = "gpt-4o-mini"
    groq_default_model: str = "llama-3.3-70b-versatile"

    # LangSmith observability
    langchain_tracing: bool = Field(
        default_factory=lambda: os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    )
    langchain_project: str = Field(
        default_factory=lambda: os.getenv("LANGCHAIN_PROJECT", "cogniflow-dev")
    )

    def validate_provider_key(self, provider: Optional[str] = None) -> None:
        """Validate that the required API key for the selected provider is present."""
        target_provider = (provider or self.default_provider).lower()
        if target_provider == "google" and not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set. Please set it in your .env file or environment.\n"
                "You can get a free key at: https://aistudio.google.com/"
            )
        elif target_provider == "openai" and not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your .env file or environment."
            )
        elif target_provider == "groq" and not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it in your .env file or environment.\n"
                "You can get a free key at: https://console.groq.com/"
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton instance of application settings."""
    return Settings()
