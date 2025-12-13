from pathlib import Path
from typing import ClassVar, Optional

from pydantic import (
    BaseModel,
    PostgresDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s] %(levelname)-7s| %(module)10s:%(lineno)-3d - %(message)s"
)
BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiConfig(BaseModel):
    prefix: str = "https://"
    host: str = "0.0.0.0"
    port: int = 8000
    url: str = ""


class LoggingConfig(BaseModel):
    log_format: str = LOG_DEFAULT_FORMAT
    log_level: str = "DEBUG"


class BotConfig(BaseModel):
    token: str = ""


class DatabaseConfig(BaseModel):
    url: Optional[PostgresDsn] = None
    echo: bool = True

    convention: ClassVar[dict] = {  # type: ignore
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class TGAdmins(BaseModel):
    admins: list[int] = []


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    bot: BotConfig
    db: DatabaseConfig
    api: ApiConfig
    admins: TGAdmins = TGAdmins()


def get_settings() -> Settings:
    """Get application settings with error handling."""
    try:
        return Settings()  # type: ignore
    except Exception as e:
        raise RuntimeError(f"Failed to load settings: {e}") from e


settings = get_settings()
