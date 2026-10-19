from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cur_llm_provider: Literal["ollama", "openai"] = "ollama"
    cur_llm_api_key: SecretStr = SecretStr("ollama")
    cur_llm_base_url: str = "http://localhost:11434"
    cur_llm_model: str = "llama3.1"
    cur_llm_temperature: float = Field(default=0.0, ge=0.0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()