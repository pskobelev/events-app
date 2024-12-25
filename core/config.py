import os

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# Вычисляем абсолютный путь к .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class LoggingConfig(BaseModel):
    log_format: str = LOG_DEFAULT_FORMAT


class BotConfig(BaseModel):
    token: str


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True


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


settings = Settings()