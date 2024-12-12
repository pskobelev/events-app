from functools import lru_cache
from logging import getLogger
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Получаем путь к корню проекта, независимо от того, из какого файла запускается приложение
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_FILE = str(BASE_DIR / ".env")
log = getLogger(__name__)

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    # DB
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Postgres
    POSTGRES_DSN: str | PostgresDsn
    # SQL ECHO
    DEBUG: bool = True

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
        return f"http://{self.API_HOST}:{self.API_PORT}"


@lru_cache
def get_config() -> Config:
    log.info("Loading config.")
    return Config()
