from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env"


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    # DB
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Postgres
    POSTGRES_DSN: PostgresDsn

    # Bot
    BOT_TOKEN: str
    ADMINS_IDS: list[int] = []

    # API
    API_NAME: str = "Event App"
    API_V1_STR: str = "/api/v1"
    API_HOST: str
    API_PORT: int

    @property
    def WEBHOOK_PATH(self) -> str:
        return f"{self.API_V1_STR}/webhook"

    @property
    def API_PATH(self) -> str:
        return f"http://{self.API_HOST}:{self.API_PORT}/"


@lru_cache
def get_config() -> Config:
    return Config()
