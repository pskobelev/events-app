import logging

import uvicorn
from fastapi import FastAPI

from src.api.events.views import router
from src.config import settings

LOGGING_DEBUG = logging.DEBUG
logging.basicConfig(level=LOGGING_DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    try:
        logger.info(
            "Starting server at %s:%d", settings.run.host, settings.run.port
        )
        logger.info("Database URL: %s", settings.db.url)
        uvicorn.run(
            "main:app",
            host=settings.run.host,
            port=settings.run.port,
            reload=True,
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Failed to start server: %s", e)
        raise
