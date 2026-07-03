from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    deepseek_api_key: str = Field(default="", alias="DEEPSEEK_API_KEY")
    deepseek_base_url: str = Field(
        default="https://api.deepseek.com",
        alias="DEEPSEEK_BASE_URL",
    )
    deepseek_model: str = Field(default="deepseek-v4-flash", alias="DEEPSEEK_MODEL")
    wingman_max_tokens: int = Field(default=500, alias="WINGMAN_MAX_TOKENS")
    wingman_temperature: float = Field(default=0.7, alias="WINGMAN_TEMPERATURE")

    price_input_per_million: float = 0.14
    price_output_per_million: float = 0.28
    price_cache_hit_per_million: float = 0.0028


@lru_cache
def get_settings() -> Settings:
    return Settings()
