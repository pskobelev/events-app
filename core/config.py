import os
from typing import ClassVar

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# Вычисляем абсолютный путь к .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class LoggingConfig(BaseModel):
    log_format: str = LOG_DEFAULT_FORMAT


class BotConfig(BaseModel):
    token: str


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True

    convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        case_sensitive=False,
    )

    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    bot: BotConfig
    db: DatabaseConfig
    api: ApiConfig = ApiConfig()


settings = Settings()