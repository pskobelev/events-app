import logging

import uvicorn
from fastapi import FastAPI

from src.api.events.views import router
from src.config import settings

logging.basicConfig(level=logging.DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)
app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host=settings.run.host,
            port=settings.run.port,
            reload=True,
        )
        logger.warning("CURRENT DB URL: %s", settings.db.url)
    except KeyboardInterrupt:
        print("App stopped by user. Goodbye!")
