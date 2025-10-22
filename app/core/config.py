# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    APP_NAME: str = "MobilitySoft — Serveur de prédiction de trafic (FR)"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_PER_MIN: int = 60
    MODEL_SEED: int = 42


settings = Settings()
