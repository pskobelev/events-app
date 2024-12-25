from pydantic import BaseModel, PostgresDsn
from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


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
        env_file="/Users/pskobelev/Developer/_PROJECTS/event_app/.env",
        case_sensitive=False,
    )

    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    bot: BotConfig = BotConfig(token="")
    db: DatabaseConfig = DatabaseConfig(
        url="postgresql+asyncpg://admin:qwe123@192.168.1.140:5432/events")

settings = Settings()
